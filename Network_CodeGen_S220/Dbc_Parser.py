import pickle
import sys,re 
from py2compat import Py2Dict

#note - class  dbc_parser not completed 
class dbc_parser:

    def __init__(self,dbc=None,node=None):
        self.dbc=dbc
        self.node=node
        self.__message=Py2Dict() #message is a dictionary which has message id(in decimal) as key and the value will also be a dictionary which contains its attributes and signal list.
        self.__multiplex_message=Py2Dict() #multiplex message is a dictionary which has message id(in decimal) as key and the value will also be a dictionary which contains its attributes and signal list.
        self.__nodes=[]#contains the nodes in the database 
        self.__message_type=[]#
        self.__message_parameters=[]#list contains what are the properties of messages defined in the database
        self.__signal_parameters=[]#list contains what are the properties of signals defined in the database
        self.__default_values=Py2Dict()
        self.__enum_values=Py2Dict()

    def __parse_messages__(self):
        '''Function uesd to extract messages,signals,message properties and signal properites
           input  dbc-database name -eg: Honda.dbc
                  node-Node for which you want to extract message and signals eg:METER
           output message - dictionary contains the data in following format
                  message={'123':{'msg_name':
        '''
        
        if self.dbc != None:
            temp_file=open(self.dbc,'r',encoding='latin-1')
            for line in temp_file:#iterate over every line in dbc file
                line=line.rstrip(' ;\n')#remove ;\n symbol on the right end line
                line=line.split(" ")#split the line into items seprated by spaces
                line = [x for x in line if (x != " " and x!='' and x!="\"\"" and x!="" and x!="''" )]#remove any spaces or '' or "" in the list 
                
                if(len(line) != 0):
                    
                    #Getting message type whicha are defined in the database 
                    '''if "BA_DEF_" in line and ("\"GenMsgSendType\"" in line or "GenMsgSendType" in line):
                        start_idx=line.index("ENUM")+1 
                        for j in range(start_idx,len(line)):
                            message_type.append(line[j])'''
                            
                    #Getting node list from the dbc 
                    if "BU_:" in line:
                        '''BU_: in dbc will define the list of nodes used in the dbc
                            Eg: BU_: Vector__XXX TCU
                                Here two nodes has been defined in database'''
                        for j in range(1,len(line)):
                            self.__nodes.append(line[j])
                            
                    #Getting Default values 
                    if "BA_DEF_DEF_" in line and len(line) > 1:
                        '''BA_DEF_DEF_  "GenMsgILSupport" "Yes";
                           GenMsgILSupport message parameter default value is Yes.
                           if not defined along with other parameters, this value will be used'''

                        line[1]=line[1].rstrip('\"').lstrip('\"')
                        if (len(line) == 2):
                            self.__default_values[line[1]]=""
                        else:
                            self.__default_values[line[1]]=line[2].rstrip('\"').lstrip('\"')
                        
                    #Getting message parameters which are defined in the database 
                    if "BA_DEF_" in line and "BO_" in line:
                        '''BA_DEF_ BO_ --> defines the parameters for each messages in the database
                           Eg: BA_DEF_ BO_  "GenMsgNrOfRepetitions" INT 0 65535;
                               BA_DEF_ BO_ "GenMsgDelayTime" INT 0 65535;
                               BA_DEF_ BO_  "GenMsgStartDelayTime" INT 0 65535;
                           here GenMsgNrOfRepetitions,GenMsgDelayTime,GenMsgStartDelayTime are the 
                           parameters defined for each messages in the list '''
                        start_idx=2
                        parameter=' '
                        for j in range(start_idx,len(line)):
                            if line[j]!=' ' and line[j]!='' and line[j]!=';' and start_idx!=0:
                                parameter = line[j].rstrip('\"').lstrip('\"')
                                self.__message_parameters.append(line[j].rstrip('\"').lstrip('\"'))
                                start_idx=0
                        
                        if "ENUM" in line:
                            #print line[line.index("ENUM")+1:]
                            par=(line[line.index("ENUM")+1:][0]).split(',')
                            enum_value=[]
                            for items in par:
                                enum_value.append(items.rstrip('\"').lstrip('\"'))
                            self.__enum_values[parameter] = enum_value
                            
                            
                    #Getting Signal parameters which are defined in the database 
                    if "BA_DEF_" in line and "SG_" in line:
                        '''BA_DEF_ SG_  --> defines the parameters for each signals in the database
                           Eg: BA_DEF_ SG_  "GenSigCycleTimeActive" INT 0 65535;
                               BA_DEF_ SG_  "GenSigCycleTime" INT 0 65535;
                               here GenSigCycleTimeActive,GenSigCycleTime are the parameters defined
                               for each messages in the list'''
                        start_idx=2
                        for j in range(start_idx,len(line)):
                            if line[j]!=' ' and line[j]!='' and line[j]!=';' and start_idx!=0:
                                self.__signal_parameters.append(line[j].rstrip('\"').lstrip('\"'))
                                start_idx=0
                    
                    '''Generally message definition starts with BO_ and signal definition starts with SG_
                       Signals of the  messages are defined under it
                           Eg: BO_ 1449 TCU_OUT1: 8 TCU
                                 SG_ TCU_REMOTE_ENG_RQ : 0|2@1+ (1,0) [0|0] "" Vector__XXX
                                 SG_ TCU_CHK_NUM : 8|8@1+ (1,0) [0|0] "" Vector__XXX
                           Here message TCU_OUT1 has two signals TCU_REMOTE_ENG_RQ and TCU_CHK_NUM
                           Message definition: BO_ 1449 TCU_OUT1: 8 TCU
                           1449 - message id in decimal
                           TCU_OUT1     ==> message name
                           8            ==> message DLC 
                           TCU          ==> Message Transmitter Node
                           Signal definition: SG_ TCU_REMOTE_ENG_RQ : 0|2@1+ (1,0) [0|0] "describes eng status" Vector__XXX
                           TCU_REMOTE_ENG_RQ ==> Signal name 
                           A|B@CD       ==> A-End bit position(0-63)
                                            B-Signal lenght(0-63)
                                            C-Bit alignment 0-Motorola 1- Intel
                                            D-signal datatype "+" means signed,"-" means unsigned
                          (E,F)         ==> E-Factor of the signal 
                                            F-Offset of the signal
                          [G|H]         ==> G-Min value of the signal
                                            H-Max value of the signal
                          "STRING"      ==> describes the purpose of the signal
                          "Vector__XXX" ==> Nodes which receives these signal'''
                                                      
                    if "BO_" in line and self.node in line and 'CM_' not in line:
                        #Getting Tx message of node by checking if B0_ and Our node name in the line list 
                        if line[1] not in self.__message:#adding new key in message dictionary with id as key  
                            self.__message[line[1]]=Py2Dict([("Multiplex","NO"),("Msg_name",line[2].rstrip(':')),("DLC",line[3]),("DIR",'tx')])
                        
                        #Below logic used for Tx signal extracting
                        signal_end=1#variable used to check the end of the signals under the paricular message
                        sig = next(temp_file)#dbc.next() will give the next line 
                        sig_list=Py2Dict()#variable used to store the signal parameter list 
                        
                        while signal_end!=0:#checking for line with SG_
                            if "BO_" in sig:#if BO_ has occured then next message definition has occured. Hence we need to stop extracting signals
                                signal_end=0
                            elif "SG_" in sig :#SG_ represents signal definition
                                #striping ';\n' , ' ', from the line
                                #print sig
                                sig=sig.rstrip(' ;\n')
                                sig=sig.lstrip(' ')
                                sig=sig.split(" ")
                                sig = [x for x in sig if (x != " " or x!="\"\"" or x!="" or x!="\'\'")] #removing all the unwanted characters from signal list 
                                
                                if sig != [] and sig.index("SG_") == 0:#checking for empty lines 
                                    temp_sig=[x for x in sig if x.find('@')>0]
                                    temp_sig_len=(temp_sig[0].split("|")[1]).split("@")[0]
                                    
                                    temp_order = ((temp_sig[0].split("|")[1]).split("@")[1]).split("+")[0]
                                    #print temp_order
                                    if '-' in temp_order:
                                        temp_order=temp_order.split('-')[0]
                                    if  temp_order in ['1',1] :
                                        temp_byte_order="Intel"
                                    else:
                                        temp_byte_order="Motorola"
                                    
                                    temp_end_bit=temp_sig[0].split("|")[0]
                                    #sig_list.append({'name':sig[1],'len':temp_sig_len,'order':temp_byte_order,'endbit':temp_end_bit})
                                    sig_list[(sig[1].rstrip(':')).upper()]=Py2Dict([('Len',temp_sig_len),('Order',temp_byte_order),('Endbit',temp_end_bit)])
                                    #print temp_byte_order
                                sig = next(temp_file) 
                                
                                #print temp_byte_order
                            else:#empty lines 
                                signal_end=0
                                
                        if line[1] not in self.__message:#adding signal list parameters to the signal
                            self.__message[line[1]]=Py2Dict([('Sig_List',sig_list)])
                        else:
                            self.__message[line[1]]['Sig_List']=sig_list
                        
                    #Getting Rx messages and Rx signals
                    #For Rx signal in message definition the node should not be our node
                    #logic used to extract rx signal list is same as tx signal list 
                    
                    if "BO_" == line[0] and self.node not in line:#checking for BO_ and other node value
                        #print line    
                        signal_end=1
                        sig = next(temp_file)
                        
                        rx_message=0#used to indicate rx message .If any signal has receiver node as our node then that message will be considered as receive message
                        multiplex_message = 0
                        sig_list=Py2Dict()
                        multiplex_rx=[]
                        multiplex_msg=Py2Dict()
                            
                        while signal_end!=0:
                            #print sig ,'SG_' in sig
                            
                            if "SG_" in sig or " SG_ " in sig:
                                #print sig
                                sig=sig.rstrip(' ;\n')
                                sig=sig.lstrip(' ')
                                sig=sig.split(" ")
                                
                                sig = [x for x in sig if (x != " " or x!="\"\"" or x!="" or x!="\'\'")]
                                
                                if self.node in sig[len(sig)-1].split(','):#if signal receiver node is our node then it is an Rx message
                                    rx_message=1
                                    if re.match('m*[0-9]',sig[2]) is not None or sig[2] == 'M':
                                      multiplex_message = 1
                                      #print sig[1]
                                      
                                      
                                    temp_sig=[x for x in sig if x.find('@')>0]
                                    temp_sig_len=(temp_sig[0].split("|")[1]).split("@")[0]
                                    temp_order = (temp_sig[0].split("|")[1].split("@")[1]).split('+')[0]
                                    if '-' in temp_order:
                                        temp_order=temp_order.split('-')[0]
                                    if temp_order in ['1',1] :
                                        temp_byte_order="Intel"
                                    else:
                                        temp_byte_order="Motorola"
                                    
                                    temp_end_bit=temp_sig[0].split("|")[0]
                                    if re.match('m*[0-9]',sig[2]) is not None:	
                                      sig_list[sig[1].rstrip(':').upper()]=Py2Dict([('Mul_order',sig[2].lstrip('m')),('Len',temp_sig_len),('Order',temp_byte_order),('Endbit',temp_end_bit)])
                                    elif sig[2] == 'M':
                                      sig_list[sig[1].rstrip(':').upper()]=Py2Dict([('Mul_order',"root"),('Len',temp_sig_len),('Order',temp_byte_order),('Endbit',temp_end_bit)])
                                    else:
                                      sig_list[sig[1].rstrip(':').upper()]=Py2Dict([('Len',temp_sig_len),('Order',temp_byte_order),('Endbit',temp_end_bit)])
                                sig = next(temp_file)
                            elif "BO_" in sig:
                                #print '1.exit'
                                signal_end=0
                            else:
                                #print '2.exit'
                                signal_end=0
                                #sig = temp_file.next()
                                
                        #print line[2].rstrip(':'),rx_message
                        if(rx_message==1):
                            if multiplex_message == 1:
                              if line[1] not in self.__multiplex_message:
                                self.__multiplex_message[line[1]]=Py2Dict([("Msg_name",line[2].rstrip(':')),("Multiplex","YES"),("DLC",line[3]),("DIR",'rx'),("Sig_List",sig_list)])
                            if line[1] not in self.__message:
                              if multiplex_message == 1:
                                self.__message[line[1]]=Py2Dict([("Msg_name",line[2].rstrip(':')),("DLC",line[3]),("Multiplex","YES"),("DIR",'rx'),("Sig_List",sig_list)])
                              else:
                                self.__message[line[1]]=Py2Dict([("Msg_name",line[2].rstrip(':')),("DLC",line[3]),("Multiplex","NO"),("DIR",'rx'),("Sig_List",sig_list)])     

        #print self.__message    
        temp_file.close()
        
    def get_multiplex(self,msg_id):
      '''This function will returnt the multiplex signal details 
        input : msgid'''
      if msg_id in self.__multiplex_message:
        multiplex_data=Py2Dict([('Multiplexor',None),('Multiplex_group',None),('Multiplex_maxval',0),('Multiplex_group_Name',None)])
        mes=self.__multiplex_message[msg_id]
        #mul_group={'Group_Name':None,'Group_list':None}
        multiplex_list=[]
        multiplex_value=0
        root=None
        
        for sig in mes['Sig_List']:
          if mes['Sig_List'][sig]['Mul_order'] !='root':
            if int(mes['Sig_List'][sig]['Mul_order']) > multiplex_value:
              multiplex_value=int(mes['Sig_List'][sig]['Mul_order'])
        if multiplex_value!=0:
          for i in range(multiplex_value+1):
            multiplex_list.append([])
            
        for sig in mes['Sig_List']:
          if mes['Sig_List'][sig]['Mul_order'] !='root':
            multiplex_list[int(mes['Sig_List'][sig]['Mul_order'])].append(sig)
          else:
            root=sig
            
        multiplex_data['Multiplex_maxval']=multiplex_value
        #mul_group['Group_list']=multiplex_list
        
        if root!=None:
          multiplex_data['Multiplexor']=root
          multiplex_data['Multiplex_group_Name']=root+'_DATA'
          if len(multiplex_list)>0:
            multiplex_data['Multiplex_group']=multiplex_list
          
        return multiplex_data
      else:
        return None
          
    def __message_par__(self):
        ''' Funtion used to extract the parameters of the each message '''
        if self.dbc != None:
            temp_file=open(self.dbc,'r',encoding='latin-1')
            for line in temp_file:  
                line=line.rstrip(';\n')
                line=line.split(" ")
                line = [x for x in line if (x != " " and x!="\"\"" and x!="" and x!="\'\'")]#Removing unwanted srings in the line 
                '''Message parameters is defined as follow in the dbc
                    BA_ "GenMsgSendType" BO_ 1106 1;
                    1106 - represents messsage id in decimal
                    1- represents the value of GenMsgSendType parameters'''
                    
                if "BA_" in line and "BO_" in line:#checkin BA_ and BO_ for message parameters
                    if line[1].rstrip('\"').lstrip('\"') in self.__message_parameters:#message_parameters list contains message parameters defined in the database file .
                            if line[3] in self.__message:
                                #rstrip and lstrip are used to remove " symbol in the string name
                                self.__message[line[3]][line[1].rstrip('\"').lstrip('\"')]=line[4].rstrip('\"').lstrip('\"')
            temp_file.close()

    def __sig_par__(self):
        '''Funtion used to extract the parameters of the each signals'''
        if self.dbc != None:
            temp_file=open(self.dbc,'r',encoding='latin-1')
            for line in temp_file:  
                    line=line.rstrip(';\n')
                    line=line.split(" ")
                    line = [x for x in line if (x != " " or x!="\"\"" or x!="")]#Removing unwanted srings in the line 
                    '''Signal parameters is defined as follow in the dbc
                        BA_ "GenSigStartValue" SG_ 1060 IGN_STAT 0;
                        1060 - represents messsage id to which signal belongs
                        IGN_STAT - Signal Name
                        0- represents the value of GenSigStartValue parameter'''
                    if "BA_" in line and "SG_" in line:#checking for BA_ and SG_ symbol in line for signal parameters
                        if line[1].rstrip('\"').lstrip('\"') in self.__signal_parameters:#signal_parameters list contains signal parameters defined in the database file 
                                if line[3] in self.__message:
                                    if line[4] in self.__message[line[3]]['Sig_List']:
                                        #rstrip and lstrip are used to remove " symbol in the string name
                                       self.__message[line[3]]['Sig_List'][line[4]][line[1].rstrip('\"').lstrip('\"')]=line[5].rstrip('\"').lstrip('\"')
            temp_file.close()

    def __add_default_message_parameters(self):
        
        for keys in self.__message:
            for prop in self.__default_values:
                #print self.__message_parameters
                if prop in self.__message_parameters and prop not in self.__message[keys]:
                    self.__message[keys][prop]=self.__default_values[prop]
                    #print self.__message  
    
    def __add_default_signal_parameters(self):         
        for keys in self.__message:
            for prop in self.__default_values:
                #print self.__message_parameters
                for signals in self.__message[keys]['Sig_List']:
                    if prop in self.__signal_parameters and prop not in self.__message[keys]['Sig_List'][signals]:
                        self.__message[keys]['Sig_List'][signals][prop]=self.__default_values[prop]
                        
    #SystemSignalLongSymbol
    def __replace_signal_name_32_bit_wide(self):
        '''self.__parse_messages__()
        self.__message_par__()
        self.__sig_par__()
        self.__add_default_message_parameters()
        self.__add_default_signal_parameters()'''
        
        if self.__message!= None and self.__message != {}:
            for mes in self.__message:
                if 'SystemMessageLongSymbol' in self.__message[mes]:
                    if self.__message[mes]['SystemMessageLongSymbol'] != '':
                        self.__message[mes]['Msg_name'] = self.__message[mes]['SystemMessageLongSymbol']
                item_to_remove=[]
                items_to_add=Py2Dict()
                for sig in self.__message[mes]['Sig_List']:
                    #print sig print 'adf'
                    #print self.__message[mes]['Sig_List'][sig]
                    if 'SystemSignalLongSymbol' in self.__message[mes]['Sig_List'][sig]:
                        if self.__message[mes]['Sig_List'][sig]['SystemSignalLongSymbol'] != '':
                            temp= self.__message[mes]['Sig_List'][sig]
                            temp_sig_name=self.__message[mes]['Sig_List'][sig]['SystemSignalLongSymbol']
                            items_to_add[temp_sig_name]=temp
                            item_to_remove.append(sig)
                            
                if item_to_remove != []:
                    for sig_remove in item_to_remove:
                        del self.__message[mes]['Sig_List'][sig_remove]

                if items_to_add!={}:
                    for sig_add in items_to_add:
                        self.__message[mes]['Sig_List'][sig_add]=items_to_add[sig_add]
                    #print self.__message[mes]['Sig_List']
        
    def create_pickle(self,name):
        '''Function used to create python pickle file
           no of parameters - 1(filename)
        '''
        self.__parse_messages__()
        self.__message_par__()
        self.__sig_par__()
        self.__add_default_message_parameters()
        self.__add_default_signal_parameters()
        self.__replace_signal_name_32_bit_wide()
        t_messages=Py2Dict()
        
           
        for keys in self.__message:
            t_messages[self.__message[keys]['Msg_name'].rstrip(':')]=self.__message[keys]
            t_messages[self.__message[keys]['Msg_name'].rstrip(':')]['idx']=hex(int(keys))
        
        pickle_file = open(name+'.p', 'wb')#creating a pickle file in name of nodes
        pickle.dump(t_messages, pickle_file) # write the pickled data to the file jar
        pickle_file.close()
        
        
    def set_dbc(self,filename):
        '''set dbc file for the object'''
        self.dbc=filename
    
    def set_node(self,nodename):
        '''set node name for the object'''
        self.node=nodename
        
    def get_node(self):
        '''returns node name for the object'''
        return self.node
        
    def get_dbc():
        '''returns dbc file for the object'''
        return self.dbc
    
    def mes_count(self,type):
        self.__parse_messages__()
        self.__parse_messages__()
        self.__message_par__()
        self.__sig_par__()
        self.__add_default_message_parameters()
        self.__add_default_signal_parameters()
        self.__replace_signal_name_32_bit_wide()
        count = {'tx':0,'rx':0,'all':0} 
        if self.__message != None:
            count['all']=len(self.__message)
            for keys in self.__message:
            
                if self.__message[keys]['DIR']=='tx':
                    count['tx']=count['tx']+1
                elif self.__message[keys]['DIR']=='rx':
                    count['rx']=count['rx']+1     
                else:
                    pass
                    
        return count[type]
    
    def msg_name(self,type):
        self.__parse_messages__()
        self.__replace_signal_name_32_bit_wide()
        count = {'tx':[],'rx':[],'all':[]}
        ms_name=[]
        if self.__message != None:
            #count['all']=len(self.__message)
            for keys in sorted(self.__message):
                if self.__message[keys]['DIR']=='tx':
                    count['tx'].append(self.__message[keys]['Msg_name'])
                elif self.__message[keys]['DIR']=='rx':
                    count['rx'].append(self.__message[keys]['Msg_name'])  
                else:
                    pass
                count['all'].append(self.__message[keys]['Msg_name'])
            #print count    
        return count[type]
    
    def get_IL_rx_id(self):
        self.__parse_messages__()
        self.__message_par__()
        self.__sig_par__()
        self.__add_default_message_parameters()
        self.__add_default_signal_parameters()
        self.__replace_signal_name_32_bit_wide()
        rx_il_message_idx=[]
        #for x in self.__message['761']:
        #    print x,self.__message['761'][x] 
        if self.__message != None:
            for keys in self.__message:
                
                if self.__message[keys]['DIR'] == 'rx':
                    #rx_il_message_idx.append(keys)
                    
                    if self.__message[keys]['GenMsgILSupport']== 'Yes':
                        rx_il_message_idx.append(keys)
                        pass
       
        else:
            rx_il_message_idx=0
        
        return rx_il_message_idx
    
    def get_enum_values(self):
        self.__parse_messages__()
        return self.__enum_values
        
    def get_msg_type(self,type,dir):
        msg_type={'IL':[],'TP':[],'NM':[],'ALL':[]}
        self.__parse_messages__()
        self.__message_par__()
        self.__sig_par__()
        self.__add_default_message_parameters()
        self.__add_default_signal_parameters()
        self.__replace_signal_name_32_bit_wide()
        temp_type=None
        #print self.__message
        if self.__message != None:
                for keys in sorted(self.__message):
                    #print self.__message[keys]
                    self.__message[keys]['id']=keys
                    if type in self.__message[keys]:
                        if self.__message[keys]['DIR'] == dir:
                            #msg_type['ALL'].append(self.__message[keys])
                            if self.__message[keys][type] in ['Yes','1',1,'yes']:
                                temp_type='IL'
                                msg_type['IL'].append(self.__message[keys])
                            elif (self.__message[keys][type] in ['Yes','1',1,'yes']):
                                temp_type='TP'
                                msg_type['TP'].append(self.__message[keys])
                            elif self.__message[keys][type] in ['Yes','1',1,'yes']:
                                temp_type='NM'
                                msg_type['NM'].append(self.__message[keys])
                                
                            
                            else:
                                pass
                    else:
                        if type.upper() == 'ALL':
                          if self.__message[keys]['DIR'] == dir:
                            msg_type['ALL'].append(self.__message[keys])
                        #raise ValueError('Invalid Parameter check property value in dbc')
                        pass
                        
                try:
                    if temp_type != None:
                        return msg_type[temp_type]
                    else:
                        if type.upper() == 'ALL':
                          #print 'dbc',msg_type['ALL']
                          return msg_type['ALL']
                        else:
                          return []
                except:
                    #print temp_type
                    #raise ValueError('Please check your database setting')
                    pass
         
        else:
            #raise ValueError('Please set dbc / check your database')
            pass
    
    def get_msg_prop(self,type,prop,dir):
        msg_type={'IL':[],'TP':[],'NM':[]}
        self.__parse_messages__()
        self.__message_par__()
        self.__sig_par__()
        self.__add_default_message_parameters()
        self.__add_default_signal_parameters()
        self.__replace_signal_name_32_bit_wide()
        temp_type=''
        
        
        if type in self.__message[keys]:
            
            if self.__message != None:
                for keys in sorted(self.__message):
                    
                    if self.__message[keys]['DIR'] == dir:
                        if self.__message[keys][type] in ['Yes','1',1,'yes'] :
                            temp_type='IL'
                            if prop != 'id':
                                msg_type['IL'].append(self.__message[keys][prop])
                            else:
                                msg_type['IL'].append(keys)
                        elif (self.__message[keys][type] in ['Yes','1',1,'yes'] ):
                            temp_type='TP'
                            if prop != 'id':
                                msg_type['TP'].append(self.__message[keys][prop])
                            else:
                                msg_type['TP'].append(keys)   
                        elif self.__message[keys][type] in ['Yes','1',1,'yes']:
                            temp_type='NM'
                            if prop != 'id':
                                msg_type['NM'].append(self.__message[keys][prop])
                            else:
                                msg_type['NM'].append(keys)   
                        else:
                            pass
                            
            return msg_type[temp_type]
        
        else:
            return None
    
    def check__node(self):
        
        try:
            self.__parse_messages__()
            #print self.node,self.__nodes
            if self.node in self.__nodes:
                return True
            else:
                return False
        except:
            return False
            
    def check_parsing(self):
        try:
            self.__parse_messages__()
            return True
        except:
            return False
        
    def __del__(self):
        del self.dbc
        del self.node
        del self.__message
        del self.__nodes
        del self.__message_type
        del self.__message_parameters
        del self.__signal_parameters
              

if __name__ =='__main__':
    #print "Module for extracting database"
    dbc=dbc_parser('U321.dbc','IS')
    x=dbc.get_msg_type('GenMsgILSupport','rx')
    '''print '-----------------------------------------'
    for i in x:
        for y in i['Sig_List']:
            print i['Sig_List'][y]['Order']
    print len(x)'''
    pass



