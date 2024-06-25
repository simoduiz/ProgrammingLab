import os #importo il modulo os che mi permette di controllare l'esistenza del file nella cartella

class ExamException( Exception ): #creo la classe per le eccezioni
    pass

class  CSVTimeSeriesFile: #creo la classe

    
    def __init__( self, name ): #la inizializzo chiedendo il file da aprire
        self.name = name #creo l'attributo name che tenga il nome del file
        
        
    def get_data( self ): #creo il metodo get_data
        test = os.path.isfile( self.name )
        if test == False:
            raise ExamException( "Errore: file non trovato" )
        f = open( self.name ) #apro il file
        records = f.readlines() #leggo il file salvando l righe in una lista
        f.close() #chiudo il file
        
        for i in range( len( records ) ): #(1)
            records[i] = records[i].split( "," ) #(2)
            try: #(**)
                
                if i != len( records )-1: #(3)
                    records[i][1] = records[i][1][1:-1]
                if records[i][1].isdigit() == True:
                    records[i][1] = int( records[i][1] )
                else:
                    raise ExamException( "Errore che non compare mai" )
                if records[i][1] <= 0:
                    raise ExamException( "Errore che non compare mai" )
            except ExamException: #(**) controllo che non ci sia una riga senza passeggeri o con un dato negativo
                records[i][1] = -1 #userò -1 come segnale di un dato non accettabile o mancante

        self.years = [] #creo una lista dove mi segno tutti gli anni che compaiono
        self.years_months =  [] #creo una lista dove mi segno tutti i mesi che compaiono
        for i in range( len( records ) ):
            self.years.append( int( records[i][0].split( "-" )[0] ) )
            self.years_months.append( records[i][0] )
        self.startyear = min( self.years ) #mi segno il primo e l'ultimo anno che compaiono in modo
        self.endyear = max( self.years ) #da individuare eventuali mesi mancanti in mezzo ai dati
        year = self.startyear #scorro per ogni mese e ogni anno dal più piccolo al più grande trovati e 

        while year <= self.endyear: #inserisco i record di tutti i mesi mancanti con un dato -1 a indicare
            for i in range( 9 ): #la mancanza di informazioni
                if str( year )+"-0"+str( i+1 ) not in self.years_months:
                    j = 12*( year-self.startyear )+i
                    records.insert( j, [str( year )+"-0"+str( i+1 ), -1] )
            i = 10
            while i < 12:
                if str( year )+"-"+str( i+1 ) not in self.years_months:
                    j = 12*( year-self.startyear )+i
                    records.insert( j, [str( year )+"-"+str( i+1 ), -1] )
                i = i+1
            year = year+1

        self.data = records #(4)

        temp = [] #copio tutti i mesi/anni in una variabile temporanea
        for i in range( len( self.years_months ) ):
            temp.append( self.years_months[i] )
        for i in range( len( self.years_months ) ): #per ogni elemento di tale lista
            year_month = temp.pop( 0 ) #elimino tale elemento e lo salvo in year_month
            if year_month in temp: #se nonostante l'eliminazione ne riesco a trovare ancora uno uguale allora è presente
                raise ExamException( "Errore: un record risulta due volte" ) #più volte e quindi torno un'eccezione
            
        temp = self.years_months[0].split( "-" )[0]
        for i in range( len( self.years_months )-1 ): #controllo che tutti gli anni riportati siano in ordine
            year = self.years_months[i+1].split( "-" )[0]
            if int( temp ) > int( year ):
                    raise ExamException( "Errore: i record non sono ordinati" )
                
            temp = year
        temp = self.years_months[0].split( "-" )[1]
        for i in range( len( self.years_months )-1 ): #controllo che tutti i mesi riportati siano in ordine
            month = self.years_months[i+1].split( "-" )[1]
            if int( temp ) > int( month ):
                if int( temp ) == 12 and int( month ) == 1:
                    pass
                else:
                    raise ExamException( "Errore: i record non sono ordinati" )
            temp = month
        
        return self.data #ritorno la lista di liste
        
        #per ogni riga letta (1) ho preso la relativa stringa (i-esimo elemento
        #della lista) e la ho splittata in 2. Il risultato è un'altra lista
        #con due elementi, anno e mese e numero di passeggeri. In particolare
        #prima avevo ["1949-01, 112\n", "1949-02, 118\n", ...] e ora ho
        #[["1949-01", "112\n"], ["1949-01", "118\n"], ...] dove i secondi
        #elementi sono sempre stringhe perché sono presenti il carattere finale
        #per mandare a capo ed uno spazio iniziale. Per risolvere il problema ho considerato esclusivamente
        #l'elemento dal secondo fino al penultimo carattere e poi ho usato il metodo isdigit per
        #capire se nella stringa ci fosse solo un numero intero o un decimale/testo/... (3)
        #A questo punto ho salvato la lista di liste in un
        #nuovo attributo chiamato data (4).
    

#creo la funzione per comparare i mesi di due anni consecutivi
def detect_similar_monthly_variations( time_series, years ):
    if years[0] != years[1]-1 and years[0] != years[1]+1: #controllo che gli anni inseriti siano consecutivi
        print( "Gli anni richiesti non sono consecutivi; si considera il primo dei due e quello consecutivo" )
        years[1] = years[0]+1 #se gli anni non sono consecutivi avviso l'utente e attuo una correzione

    #ripeto la procedura usata per identificare tutti gli anni presenti nella time series
    years_ = [] #creo una lista dove mi segno tutti gli anni che compaiono
    for i in range( len( time_series ) ):
        years_.append( int( time_series[i][0].split( "-" )[0] ) )

    if years[0] not in years_ or years[1] not in years_:
        raise ExamException( "Errore: gli anni inseriti non sono validi" )
    
    anno1 = [] #creo due liste che terranno i dati mensili dei due anni
    anno2 = []
    variazioni1 = [] #creo le due liste che terranno le 11 variazioni degli anni
    variazioni2 = []
    risultati = [] #creo la lista che terrà i risultati (true/false)

    for i in range( len( time_series ) ): #per ogni dato nella lista di liste
        if str( years[0] )+"-01" in time_series[i]: #cerco il primo mese del
            start = i #primo anno e mi segno la sua posizione
            break #fermo il ciclo di ricerca
    for i in range( 12 ): #inserisco nella prima lista i dati del primo anno
        anno1.append( time_series[start+i][1] )
        
    for i in range( len( time_series ) ): #ripeto la procedura per il secondo
        if str( years[1] )+"-01" in time_series[i]:
            start = i
            break
    for i in range( 12 ):
        anno2.append( time_series[start+i][1] )

    for i in range( 11 ): #per ogni coppia di mesi salvo la differenza nella
        variazioni1.append( abs( anno1[i+1]-anno1[i] ) ) #rispettiva lista di
        variazioni2.append( abs( anno2[i+1]-anno2[i] ) ) #variazioni
        if abs( variazioni2[i]-variazioni1[i] ) <= 2: #se tale differenza è #al massimo 2 in valore assoluto allora
            if anno1[i+1] != -1 and anno1[i] != -1 and anno2[i+1] != -1 and anno2[i] != -1:
                risultati.append( True )
            else:
                risultati.append( False ) #se uno dei mesi coinvolto non era presente allora assumo sia False
        else: #salvo il valore true nella lista di risultati; altrimenti salvo
            risultati.append( False ) #il valore false.

    return risultati #ritorno la lista di risultati
