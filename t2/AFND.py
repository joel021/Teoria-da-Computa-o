import numpy as np

class AFND():

    class State():
        
        def __init__(self, name):
            """
            @name: (String) key name of the state
            """
            self.name = name #
            self.dest = dict() #(Dict) "destiny" is the next states when receiving a valid character.
            self.is_final_state = "N"
            self.processed = False
            self.eq_states = []
            
    def __init__(self ):
        self.afd_states = None
    
    def _input_E(self, in_i):
        self.E = str(in_i).split(" ")
        
    def _construct_states(self):
        states = dict()
        
        for e in self.E:
            states[e] = self.State(e) #create a state instance to each state
        return states
    
    def _input_sigma(self, in_i):
        self.sigma = str(in_i).split(" ")
    
    def _input_n(self, in_i):
        self.n = int(in_i)
        
    def _ext_trans_func(self, word):
        """
        extended transaction function (delta)
        @characters: (List) list of characters to be processed
        """
        state = self.afd_states[self.init_state_k]

        for c in list(word):
            k = state.dest.get(c, self.afd_states["error"]) #apply the the delta function
            state = self.afd_states[k]
            
        print(state.is_final_state)
    
    def _set_states_trctions(self, afd_states):
        
        #defining states transations: delta function
        for i in range(self.n):
            t = str(input()).split(" ") #has shape like: "o c d" -> (o, c, d) -> (orign state, character, destination state)
            
            state_i = afd_states.get(t[0]) #get reference of the state named in t[0]
            
            states = []
            states.extend(state_i.dest.get(t[1], [])) #get all possible defined transaction states to this entry
            states.append(afd_states.get(t[2],[])) #insert a destination of this state when receiving t[1] value
            
            state_i.dest[t[1]] = states #Override, if already exists. Create, if not exist.
    
    def get_eq_key_isf(self, states):
        """
        Get equivalent state to these states. 
        Ex.: Receiving states = {e1,e2,e1,e2,e3} => k = "{e1,e2,e3}"
        """
        k = set()
        is_final_state = dict()
        for s in states:
            k.add(s.name)
            is_final_state[s.is_final_state] = s.is_final_state
        k = np.sort(list(k))
        
        return str(k), is_final_state.get("S", "N")
    
    def _get_AFD(self, afnd_states, init_k):
        states = dict() #AFD states
        states["error"] = self.State("error")
        
        self.init_state_k = str([init_k])
        states[self.init_state_k] = self.State(self.init_state_k)
        states[self.init_state_k].processed = True
        k_d = [] #to store the remaining state wich must be processed
        
        #Create initial state to the AFD
        for w in self.sigma:
            
            d_states = afnd_states[init_k].dest.get(w, []) #afnd_states are needed only here to get the first state
            #get key to this state
            k, is_final_state = self.get_eq_key_isf(d_states) #all destinate states of the first state
            k_d.append(k)
            
            states[k] = states.get(k, self.State(k)) #Create or get the equivalent state
            states[k].is_final_state = is_final_state #if any state is final, this new state is final too.
            states[k].eq_states = d_states #equivalent states of this state
            
            states[self.init_state_k].dest[w] = k #set the key destination of this state when receive w
        
        #case logic to decide if process or not
        process = {
                False: self._process, 
                True: self._pass
        }
        
        while bool(k_d): #while exists states to be processed
            state = states[k_d.pop()]
            process[state.processed](state, k_d, states)
            
        self.afd_states = states
        #result: an AFD with states defined
            
    def _pass(self, *args):
        pass
    
    def _process(self, state, k_d, states):
        """
        Set all destination states of the state "state" for each w in sigma.
        Create the new equivalent state if not exists
        Set the equivalente state to be the destination
        """
        for w in self.sigma: 
            
            d_states = [] #destination states
            for e in state.eq_states:
                d_states.extend(e.dest.get(w, [])) #this state is composed by one or more states wich each has their own destination states
                
            k, is_final_state = self.get_eq_key_isf(d_states)

            states[k] = states.get(k, self.State(k)) #Get or create the state hashed with k key. The states where has it as destination do not will lost it.
            states[k].is_final_state = is_final_state
            states[k].eq_states = d_states
            
            state.dest[w] = k #store the key of this state as destination state key
            k_d.append(k) #insert the key of this "new" state to be processed
        
        state.eq_states = [] #clear this information of the processed state becouse is not necessary no more
        state.processed = True

    def init(self):
        """
        Configuration steps
        """
        #get continuos inputs to first configuration
        model = {
            0: self._input_E, #define states list
            1: self._input_sigma,
            2: self._input_n
        }
        for i in range(3):
            in_i = input()
            #configuration steps
            model[i](in_i)
        
        afnd_states = self._construct_states()
        
        self._set_states_trctions(afnd_states)
        
        #get initial state key
        init_k = str(input())
        
        #get and set final states
        for e in str(input()).split(" "):
            afnd_states[e].is_final_state = "S"
        
        #get the AFD equivalent
        self._get_AFD(afnd_states, init_k)
        
        """
        End Configuration Steps
        """
        
        #recognize the words. The AFD has not transactions on lambda
        for word in str(input()).replace(" * ", "").replace("*", "").split(" "):
            self._ext_trans_func(word)
            
afnd = AFND()
afnd.init()