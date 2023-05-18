#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Conversion of epsilon-NFA to DFA and visualization using Graphviz
 
from graphviz import Digraph
from tkinter import *
states=[]
no_of_states=0
alphabets=[]
no_of_alphabets=0
startstate=""
no_of_finalstates=0
finalstate=[]
no_of_transitions=0
trans_start=''
trans_trans=''
trans_final=''
transition_set_1=[]
tranisition_set_2=[]

def states_no():
    states.append(Statesentry.get())
    global no_of_states 
    no_of_states += 1

def alphabets_no():
    alphabets.append(Alphabetsentry.get())
    global no_of_alphabets 
    no_of_alphabets += 1

def start_state():
    global startstate 
    startstate=StartState_entry.get()

def final_state():
    global finalstate
    finalstate=FinalState_entry.get()
    global no_of_finalstates
    no_of_finalstates=no_of_finalstates+1


def drawtransition():
    global trans_start
    trans_start=start_state_entry.get()
    global trans_trans
    trans_trans=transition_entry.get()
    global trans_final
    trans_final=final_state_entry.get()
    global no_of_transitions
    no_of_transitions=no_of_transitions+1
    global transition_set_1
    global tranisition_set_2
    transition_set_1.append(trans_start)
    transition_set_1.append(trans_trans)
    transition_set_1.append(trans_final)
    tranisition_set_2.append(transition_set_1)
    transition_set_1=[]








class NFA:
    def __init__(self, no_state, states, no_alphabet, alphabets, start,
                 no_final, finals, no_transition, transitions):
        self.no_state = no_state
        self.states = states
        self.no_alphabet = no_alphabet
        self.alphabets = alphabets
         
        # Adding epsilon alphabet to the list
        # and incrementing the alphabet count
        self.alphabets.append('e')
        self.no_alphabet += 1
        self.start = start
        self.no_final = no_final
        self.finals = finals
        self.no_transition = no_transition
        self.transitions = transitions
        self.graph = Digraph()
 
        # Dictionaries to get index of states or alphabets
        self.states_dict = dict()
        for i in range(self.no_state):
            self.states_dict[self.states[i]] = i
        self.alphabets_dict = dict()
        for i in range(self.no_alphabet):
            self.alphabets_dict[self.alphabets[i]] = i
             
        # transition table is of the form
        # [From State + Alphabet pair] -> [Set of To States]
        self.transition_table = dict()
        for i in range(self.no_state):
            for j in range(self.no_alphabet):
                self.transition_table[str(i)+str(j)] = []
        for i in range(self.no_transition):
            self.transition_table[str(self.states_dict[self.transitions[i][0]])
                                  + str(self.alphabets_dict[
                                      self.transitions[i][1]])].append(
                                          self.states_dict[self.transitions[i][2]])
    
 
 
    def getEpsilonClosure(self, state):
       
        # Method to get Epsilon Closure of a state of NFA
        # Make a dictionary to track if the state has been visited before
        # And a array that will act as a stack to get the state to visit next
        closure = dict()
        closure[self.states_dict[state]] = 0
        closure_stack = [self.states_dict[state]]
 
        # While stack is not empty the loop will run
        while (len(closure_stack) > 0):
           
            # Get the top of stack that will be evaluated now
            cur = closure_stack.pop(0)
             
            # For the epsilon transition of that state,
            # if not present in closure array then add to dict and push to stack
            for x in self.transition_table[
                    str(cur)+str(self.alphabets_dict['e'])]:
                if x not in closure.keys():
                    closure[x] = 0
                    closure_stack.append(x)
            closure[cur] = 1
        return closure.keys()
 
    def getStateName(self, state_list):
       
        # Get name from set of states to display in the final DFA diagram
        name = ''
        for x in state_list:
            name += self.states[x]
        return name
 
    def isFinalDFA(self, state_list):
       
        # Method to check if the set of state is final state in DFA
        # by checking if any of the set is a final state in NFA
        for x in state_list:
            for y in self.finals:
                if (x == self.states_dict[y]):
                    return True
        return False
 
 
print("E-NFA to DFA")
 
# INPUT
# Number of States : no_state
# Array of States : states
# Number of Alphabets : no_alphabet
# Array of Alphabets : alphabets
# Start State : start
# Number of Final States : no_final
# Array of Final States : finals
# Number of Transitions : no_transition
# Array of Transitions : transitions

root = Tk()
Label(root,text="States").grid()
Statesentry=Entry(root,width=5)
Statesentry.grid()
Button(root,text="add state",command=lambda:states_no()).grid()
Label(root,text="alphabets").grid()
Alphabetsentry=Entry(root,width=5)
Alphabetsentry.grid()
Button(root,text="add alphabet",command=lambda:alphabets_no()).grid()
Label(root,text="Start state").grid()
StartState_entry=Entry(root,width=5)
StartState_entry.grid()
Button(root,text="add start state",command=lambda:start_state()).grid()
Label(root,text="Final state").grid()
FinalState_entry=Entry(root,width=5)
FinalState_entry.grid()
Button(root,text="add final state",command=lambda:final_state()).grid()
Label(root,text="start").grid()
start_state_entry=Entry(root,width=5)
start_state_entry.grid()
Label(root,text="transition").grid()
transition_entry=Entry(root,width=5)
transition_entry.grid()
Label(root,text="destintation").grid()
final_state_entry=Entry(root,width=5)
final_state_entry.grid()
Button(root,text="add transition",command=lambda:drawtransition()).grid()
root.mainloop()


nfa = NFA(
    no_of_states,  # number of states
    states,  # array of states
    no_of_alphabets,  # number of alphabets
    alphabets,  # array of alphabets
    startstate,  # start state
    no_of_finalstates,  # number of final states
    finalstate,  # array of final states
    no_of_transitions,  # number of transitions
    tranisition_set_2
   
    # array of transitions with its element of type :
    # [from state, alphabet, to state]
)
 
# nfa = NFA.fromUser() # To get input from user
# print(repr(nfa)) # To print the quintuple in console
 
# Making an object of Digraph to visualize NFA diagram
nfa.graph = Digraph()
 
for x in nfa.states:
   
    if (x not in nfa.finals):
        nfa.graph.attr('node', shape='circle')
        nfa.graph.node(x)
    else:
        nfa.graph.attr('node', shape='doublecircle')
        nfa.graph.node(x)
 
# Adding start state arrow in NFA diagram
nfa.graph.attr('node', shape='none')
nfa.graph.node('')
nfa.graph.edge('', nfa.start)
 
for x in nfa.transitions:
    nfa.graph.edge(x[0], x[2], label=('ε', x[1])[x[1] != 'e'])


 
# Makes a pdf with name nfa.graph.pdf and views the pdf
def ViewNFA():
   nfa.graph.render('nfa', view=True)



 
# Making an object of Digraph to visualize DFA diagram
dfa = Digraph()
 
# Finding epsilon closure beforehand so to not recalculate each time
epsilon_closure = dict()
for x in nfa.states:
    epsilon_closure[x] = list(nfa.getEpsilonClosure(x))
 
 
# First state of DFA will be epsilon closure of start state of NFA
# This list will act as stack to maintain till when to evaluate the states
dfa_stack = list()
dfa_stack.append(epsilon_closure[nfa.start])
 
# Check if start state is the final state in DFA
if (nfa.isFinalDFA(dfa_stack[0])):
    dfa.attr('node', shape='doublecircle')
else:
    dfa.attr('node', shape='circle')
dfa.node(nfa.getStateName(dfa_stack[0]))
 
# Adding start state arrow to start state in DFA
dfa.attr('node', shape='none')
dfa.node('')
dfa.edge('', nfa.getStateName(dfa_stack[0]))
 
# List to store the states of DFA
dfa_states = list()
dfa_states.append(epsilon_closure[nfa.start])
 
# Loop will run till this stack is not empty
while (len(dfa_stack) > 0):
    # Getting top of the stack for current evaluation
    cur_state = dfa_stack.pop(0)
 
    # Traversing through all the alphabets for evaluating transitions in DFA
    for al in range((nfa.no_alphabet) - 1):
        # Set to see if the epsilon closure of the set is empty or not
        from_closure = set()
        for x in cur_state:
            # Performing Union update and adding all the new states in set
            from_closure.update(
                set(nfa.transition_table[str(x)+str(al)]))
 
        # Check if epsilon closure of the new set is not empty
        if (len(from_closure) > 0):
            # Set for the To state set in DFA
            to_state = set()
            for x in list(from_closure):
                to_state.update(set(epsilon_closure[nfa.states[x]]))
 
            # Check if the to state already exists in DFA and if not then add it
            if list(to_state) not in dfa_states:
                dfa_stack.append(list(to_state))
                dfa_states.append(list(to_state))
 
                # Check if this set contains final state of NFA
                # to get if this set will be final state in DFA
                if (nfa.isFinalDFA(list(to_state))):
                    dfa.attr('node', shape='doublecircle')
                else:
                    dfa.attr('node', shape='circle')
                dfa.node(nfa.getStateName(list(to_state)))
 
            # Adding edge between from state and to state
            dfa.edge(nfa.getStateName(cur_state),
                     nfa.getStateName(list(to_state)),
                     label=nfa.alphabets[al])
             
        # Else case for empty epsilon closure
        # This is a dead state(ϕ) in DFA
        else:
           
            # Check if any dead state was present before this
            # if not then make a new dead state ϕ
            if (-1) not in dfa_states:
                dfa.attr('node', shape='circle')
                dfa.node('ϕ')
 
                # For new dead state, add all transitions to itself,
                # so that machine cannot leave the dead state
                for alpha in range(nfa.no_alphabet - 1):
                    dfa.edge('ϕ', 'ϕ', nfa.alphabets[alpha])
 
                # Adding -1 to list to mark that dead state is present
                dfa_states.append(-1)
 
            # Adding transition to dead state
            dfa.edge(nfa.getStateName(cur_state,),
                     'ϕ', label = nfa.alphabets[al])
 
# Makes a pdf with name dfa.pdf and views the pdf
def ConvertToDFA():
     dfa.render('dfa', view = True)

subroot=Tk()
Button(subroot,text="view NFA",command=lambda:ViewNFA()).grid()
Button(subroot,text="Convert to DFA",command=lambda:ConvertToDFA()).grid()
subroot.mainloop()


# In[ ]:





# In[ ]:




