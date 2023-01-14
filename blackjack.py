import simplegui
import random

CANVAS=(600,600)
margin=2

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    


in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
#    The __init__ method should initialize the Hand object to have an empty list of Card objects. 
#    The __str__ method should return a string representation of a Hand object in a human-readable form. 
    
    def __init__(self):
        self.hands=[]

    def __str__(self):
        ans = ""
        for i in range(len(self.hands)):
            ans += str(self.hands[i])+' '
        return 'hand contains '+ans

    def add_card(self, card):
        self.hands.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_val=0
        isace=False
        for card in self.hands:
            hand_val+=VALUES[card.get_rank()]
            if card.get_rank()=='A':
                isace=True
        if isace and hand_val<=11:
            hand_val+=10
        return hand_val	
   
    def draw(self, canvas, pos):
        card_count=0
        
        for card in self.hands:
            if card_count<5:
                card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card.get_rank()), 
                            CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card.get_suit()))
                canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0]+card_count*CARD_SIZE[0]+margin, pos[1] + CARD_CENTER[1]], CARD_SIZE)
                card_count+=1
    

        
# define deck class 
class Deck:

    def __init__(self):
        self.deck=[]
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
       random.shuffle(self.deck)    

    def deal_card(self):
        dealt=random.choice(self.deck)	
        self.deck.remove(dealt)
        return dealt
        
    def __str__(self):
        ans = ""
        for i in range(len(self.deck)):
            ans += str(self.deck[i])+' '
        return 'deck contains '+ans	




#define event handlers for buttons
def deal():
    global score,outcome, in_play,Deck_inplay,Player_Hand, Dealer_Hand

    if in_play:
        outcome='Dealer wins. Hit or Stand?'
        score-=1
    else:
        outcome='Hit or Stand?'
    
    Deck_inplay=Deck()
    Deck_inplay.shuffle()
    
    Player_Hand=Hand()
    Dealer_Hand=Hand()
    
    for i in range(0,2):
        Player_Hand.add_card(Deck_inplay.deal_card())
        Dealer_Hand.add_card(Deck_inplay.deal_card())
        
    in_play = True
    

def hit():
    global score,outcome,in_play,Deck_inplay,Player_Hand   
    
    if in_play:
        if Player_Hand.get_value()<21:
            Player_Hand.add_card(Deck_inplay.deal_card())
            if Player_Hand.get_value()>21:
                #print "You have busted"
                outcome='You have busted.  New deal?'
                score-=1
                in_play = False
        else:
            outcome='Hit or Stand?'
        
       
def stand():
        global score,outcome,in_play,Deck_inplay,Player_Hand, Dealer_Hand   
    
        if in_play:
            if Player_Hand.get_value()>21:
                #print "You have busted"
                outcome='You have busted.  New deal?'
                score-=1
            else:
                while Dealer_Hand.get_value()<17:
                    Dealer_Hand.add_card(Deck_inplay.deal_card())
                
                if Dealer_Hand.get_value()>21:
                     #   print "Dealer has gone bust"
                        outcome='Dealer has gone bust - You win.  New deal?'
                        score+=1
                else:
                    if Player_Hand.get_value()>Dealer_Hand.get_value():
                       # print "You have won"
                        outcome='You have won.  New deal?'
                        score+=1
                    else:
                       # print "Dealer wins"
                        outcome='Dealer wins.  New deal?'
                        score-=1
            in_play=False


# draw handler    
def draw(canvas):

    BJfontsz=52
    Outfontsz=23
    textfontsz=18
    scorefontsz=30
    pos=[50,130+BJfontsz+Outfontsz+4*textfontsz+CARD_SIZE[1]]
    
    canvas.draw_text('Blackjack',[(CANVAS[0]-frame.get_canvas_textwidth('Blackjack', BJfontsz))/2, 20+BJfontsz], BJfontsz, 'Black')
    canvas.draw_text(outcome, [(CANVAS[0]-frame.get_canvas_textwidth(outcome,Outfontsz))/2, 60+BJfontsz+Outfontsz], Outfontsz, 'Red')
     
    canvas.draw_text('Player Hand:',[20,120+BJfontsz+Outfontsz+textfontsz],textfontsz,'Black')
    Player_Hand.draw(canvas, [pos[0], pos[1]-10-2*textfontsz-CARD_SIZE[1]]) 
    canvas.draw_text('Dealer Hand:',[20,130+BJfontsz+Outfontsz+3*textfontsz+CARD_SIZE[1]],textfontsz,'Black')
    Dealer_Hand.draw(canvas, [pos[0], pos[1]])
    scorestr=str(score)
    
    while len(scorestr)<5:
        scorestr=' '+scorestr
        
    scorestr='SCORE: '+ scorestr
    canvas.draw_text(scorestr,[CANVAS[0]-frame.get_canvas_textwidth(scorestr,scorefontsz)-50,CANVAS[1]-10-scorefontsz],scorefontsz,'Red')
    if in_play:
         canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [CARD_BACK_CENTER[0]+margin+pos[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", CANVAS[0], CANVAS[1])
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

