class AFD():
    
    class State():
        
        def __init__(self, name):
            """
            @name: (String) key name of the state
            """
            self.name = name #
            self.dest = dict() #(Dict) "destiny" is the next state when receiving a valid characters.
            self.is_final_state = "N"
            
    def __init__(self, ):
        self.model = {
            0: self._get_E, #define states list
            1: self._get_sigma,
            2: self._get_n
        }
    
    def _get_E(self, in_i):
        self.E = str(in_i).split(" ")
        
    def _construct_states(self):
        self.states = dict()
        
        for e in self.E:
            self.states[e] = self.State(e)
        
        #One difference to definition here. This state has not transaction
        self.states["error"] = self.State("error")
        
    def _get_sigma(self, in_i):
        self.sigma = str(in_i).split(" ")
    
    def _get_n(self, in_i):
        self.n = int(in_i)
        
    def _ext_trans_func(self, words):
        """
        extended transaction function (delta)
        @characters: (List) list of characters to be processed
        """
        for word in words:
            state = self.states[self.init_state_k]
            
            for c in list(word):
                state = state.dest.get(c, self.states["error"]) #apply the the delta function
            
            print(state.is_final_state)
            
    def init(self):        
        
        #get continuos inputs to first configuration
        for i in range(3):
            in_i = input()
            #configuration steps
            self.model[i](in_i)
        
        self._construct_states()
        
        #defining states transations: delta function
        for i in range(self.n):
            t = str(input()).split(" ") #has shape like: "o c d" -> (o, c, d) -> (orign state, character, destination state)
            
            state_i = self.states.get(t[0]) #get reference of the state named in t[0]
            state_i.dest[t[1]] = self.states.get(t[2], self.states["error"]) #define destination of this state when receiving t[1] value
            
        #get initial state key
        self.init_state_k = str(input())
        
        #get and set final states
        for e in str(input()).split(" "):
            self.states[e].is_final_state = "S"
        
        #recognize the words
        self._ext_trans_func(str(input()).split(" "))
        
#execute
adf = AFD()

adf.init()