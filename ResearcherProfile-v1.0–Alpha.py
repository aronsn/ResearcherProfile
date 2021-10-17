## Importer moduler
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import webbrowser


class MyGUI:
    def __init__(self):
        ## Opprett hovedvindu
        self.root=Tk()
        self.root.title('Researcher profile')
        self.root.configure(bg='light sky blue')

        ## Opprett loddrett scrollbar
        self.y_scrollbar=Scrollbar(self.root, orient=VERTICAL)
        self.y_scrollbar.grid(row=0, column=0, rowspan=10, padx=(8, 0), pady=(8, 0), sticky=NS)   

        ## Opprett vannrett scrollbar
        self.x_scrollbar=Scrollbar(self.root, orient=HORIZONTAL)
        self.x_scrollbar.grid(row=10, column=1, padx=(0, 8), pady=(0, 8), sticky=EW)

        ## Opprett treeview
        self.tree=ttk.Treeview(self.root, yscrollcommand=self.y_scrollbar.set, xscrollcommand=self.x_scrollbar.set)

        ## Grid ut før treeview
        self.y_scrollbar['command']=self.tree.yview
        self.x_scrollbar['command']=self.tree.xview

        ## Opprett treeviewets kolonner
        ## Her er width mindre enn minwidth: dette er fordi headeren ser ut til å påvirkes av width.
        ## Minwidth blir da den sanne vidden på kolonnen
        ## Stretch må være sann for å tillate horisontal scrolling av treeview
        ## Det er kjent at Tkinter har et problem med horisontal scroll av treeview
        ## Dette gjør at vidden på katalog-kolonen må justeres i programmet
        self.tree['columns']=('Name', 'Field', 'Date/Start date', 'Location', 'Link')
        self.tree.column('Name', width=150, minwidth=250, stretch=True)
        self.tree.column('Field', width=150, minwidth=200, stretch=True)
        self.tree.column('Date/Start date', width=150, minwidth=200, stretch=True)
        self.tree.column('Location', width=150, minwidth=200, stretch=True)
        self.tree.column('Link', width=150, minwidth=450, stretch=True)

        ## Opprett headings
        self.tree.heading('Name', text='Name')
        self.tree.heading('Field', text='Field')
        self.tree.heading('Date/Start date', text='Date/Start date')
        self.tree.heading('Location', text='Location')
        self.tree.heading('Link', text='Link')

        ## Opprett directories/kataloger
        self.dir1=self.tree.insert('', 0, 'Conferences', text='Conferences')
        self.dir2=self.tree.insert('', 1, 'Projects', text='Projects')

        ## Grid ut treeview
        self.tree.grid(row=0, column=1, rowspan=10, padx=(0, 8), pady=(8, 0), sticky=NS)

        ## Opprett cursor
        self.cur_fetch=mydatabase.cursor()

        ## Bruk cursor, hent konferanser
        self.cur_fetch.execute('''SELECT *
                                  FROM Conference''')

        ## Tellebasert løkke for å fylle treeview med konferanser
        ## Opprett teller for å holde styr på index
        self.__count=0
        for row in self.cur_fetch:
            self.__name=row[0]
            self.__field=row[1]
            self.__time=row[2]
            self.__location=row[3]
            self.__link=row[4]
            ## Insert består av navnet på directory/katalog, indeks for rad i katalogen, og verdiene som skal settes inn.
            ## Komma mellom verdiene indikerer ny kolonne.
            self.tree.insert('Conferences', self.__count, values=(self.__name, self.__field, self.__time, self.__location, self.__link))
            ## Oppdater telleren
            self.__count +=1

        ## Bruk cursor, hent prosjekter
        self.cur_fetch.execute('''SELECT *
                                  FROM Project''')

        ## Tellebasert løkke for å fylle treeview med prosjekter
        ## Opprett teller for å holde styr på index
        self.__count=0
        for row in self.cur_fetch:
            self.__name=row[0]
            self.__field=row[1]
            self.__time=row[2]
            self.__location=row[3]
            ## Insert
            self.tree.insert('Projects', self.__count, values=(self.__name, self.__field, self.__time, self.__location))
            ## Oppdater telleren
            self.__count +=1

        ## Buttons til ulike funksjoner
        self.btn_conference_add=Button(self.root, width=16, text='Add', command=self.conference_add)
        self.btn_conference_edit=Button(self.root, width=16, text='Edit', command=self.conference_edit)
        self.btn_conference_delete=Button(self.root, width=16, text='Delete', command=self.conference_confirm_delete)

        self.btn_conference_add.grid(row=1, column=2, padx=(10, 5), pady=8, sticky=W)
        self.btn_conference_edit.grid(row=2, column=2, padx=(10, 5), pady=8, sticky=W)
        self.btn_conference_delete.grid(row=3, column=2, padx=(10, 5), pady=8, sticky=W)

        self.btn_project_add=Button(self.root, width=16, text='Add', command=self.project_add)
        self.btn_project_edit=Button(self.root, width=16, text='Edit', command=self.project_edit)
        self.btn_project_delete=Button(self.root, width=16, text='Delete', command=self.project_confirm_delete)

        self.btn_project_add.grid(row=5, column=2, padx=(10, 5), pady=8, stick=W)
        self.btn_project_edit.grid(row=6, column=2, padx=(10, 5), pady=8, sticky=W) 
        self.btn_project_delete.grid(row=7, column=2, padx=(10, 5), pady=8, sticky=W)

        ## Beskrivende labels
        self.lbl_conferences=Label(self.root, width=16, bg='light sky blue', text='Conferences')
        self.lbl_projects=Label(self.root, width=16, bg='light sky blue', text='Projects')

        self.lbl_conferences.grid(row=0, column=2, padx=(10, 5), pady=8, sticky=W)
        self.lbl_projects.grid(row=4, column=2, padx=(10, 5), pady=8, sticky=W)

        ## Bind dobbeltklikk av treeview
        ## Åpner lenken i nettleser
        self.tree.bind('<Double-1>', self.callback)

        #Binder curselection til tree_select-metoden
        self.tree.bind('<ButtonRelease-1>', self.tree_select)

        # StringVar for å holde navn of tid fra tree_select
        self.__name_treeview=StringVar()
        self.__time_treeview=StringVar()

        ## Lukk cursor
        self.cur_fetch.close()

        ## Igangsett hovedløkken
        self.root.mainloop()


    ## Metode for å legge til konferanse
    def conference_add(self):
        ## Steng eventuelle andre toplevels
        try:
            self.toplevel.destroy()
        except:
            pass
        
        ## Opprett nytt vindu
        self.toplevel=Toplevel(self.root)
        ## '-topmost' sikrer at vinduet alltid ligger øverst
        self.toplevel.attributes('-topmost', 'true')
        self.toplevel.title('Add conference')
        self.toplevel.configure(bg='light sky blue')

        ## Beskrivende labels
        self.lbl_name_con_add=Label(self.toplevel, width=16, bg='light sky blue', text='Name*')
        self.lbl_field_con_add=Label(self.toplevel, bg='light sky blue', text='Field')
        self.lbl_time_con_add=Label(self.toplevel, bg='light sky blue', text='Date*') 
        self.lbl_location_con_add=Label(self.toplevel, bg='light sky blue', text='Location')
        self.lbl_link_con_add=Label(self.toplevel, bg='light sky blue', text='Link')
        self.lbl_explanation_con_add=Label(self.toplevel, bg='light sky blue', text='Entries marked with * are mandatory')

        self.lbl_name_con_add.grid(row=0, column=0, padx=8, pady=8, sticky=W)
        self.lbl_field_con_add.grid(row=0, column=1, padx=8, pady=8, sticky=W)
        self.lbl_time_con_add.grid(row=0, column=2, padx=8, pady=8, sticky=W)
        self.lbl_location_con_add.grid(row=0, column=3, padx=8, pady=8, sticky=W)
        self.lbl_link_con_add.grid(row=0, column=4, padx=8, pady=8, sticky=W)
        self.lbl_explanation_con_add.grid(row=2, column=0, padx=8, pady=8, sticky=W)

        ## Entry widgets
        self.__name_var_con_add=StringVar()
        self.ent_name_con_add=Entry(self.toplevel, width=32, textvariable=self.__name_var_con_add)
        ## Tkinter har dessverre ingen date picker, derav en enkel entry widget.
        self.__time_var_con_add=StringVar()
        self.ent_time_con_add=Entry(self.toplevel, width=16, textvariable=self.__time_var_con_add)
        self.__location_var_con_add=StringVar()
        self.ent_location_con_add=Entry(self.toplevel, width=32, textvariable=self.__location_var_con_add)
        self.__link_var_con_add=StringVar()
        self.ent_link_con_add=Entry(self.toplevel, width=32, textvariable=self.__link_var_con_add)

        self.ent_name_con_add.grid(row=1, column=0, padx=8, pady=8, sticky=W)
        self.ent_time_con_add.grid(row=1, column=2, padx=8, pady=8, sticky=W)
        self.ent_location_con_add.grid(row=1, column=3, padx=8, pady=8, sticky=W)
        self.ent_link_con_add.grid(row=1, column=4, padx=8, pady=8, sticky=W)

        ## Combobox
        self.combo=ttk.Combobox(self.toplevel, width=32, state='readonly', values=['',
                                                                                   'Big data',
                                                                                   'Open data',
                                                                                   'Software engineering',
                                                                                   'software engineering education',
                                                                                   'HCI'])
        self.combo.grid(row=1, column=1, padx=8, pady=8, sticky=W)
        self.combo.current(0)
        
                                                       

        ## Button for å lagre verdiene
        self.btn_update_con_add=Button(self.toplevel, width=16, text='Add', command=self.conference_add_commit)
        self.btn_update_con_add.grid(row=1, column=5, padx=8, pady=8, sticky=W)

        ## Igangsett hovedløkken
        self.toplevel.mainloop()


    ## Metode for å oppdatere basen med en nye konferanse
    def conference_add_commit(self):
        ## Opprett cursor for å lagre data
        self.cur_add_commit=mydatabase.cursor()

        ## Varabler som skal kunne stå tomme gis null-merke
        self.__field_con_commit=str('NULL')
        self.__location_con_commit=str('NULL')
        self.__link_con_commit=str('NULL')

        ## Variabler som skal sette i liste og executes
        self.__name_con_commit=str(self.__name_var_con_add.get())
        self.__field_con_commit=str(self.combo.get())
        self.__time_con_commit=str(self.__time_var_con_add.get())
        self.__location_con_commit=str(self.__location_var_con_add.get())
        self.__link_con_commit=str(self.__link_var_con_add.get())

        ## Query-del av execute
        self.__cursor_query_commit=('''INSERT INTO Conference
                                       (ConferenceName, ConferenceField, ConferenceTime, ConferenceLocation, Link)
                                       VALUES(%s, %s, %s, %s, %s)''')
        ## Value-del av execute
        self.__cursor_values_commit=(self.__name_con_commit,
                                     self.__field_con_commit,
                                     self.__time_con_commit,
                                     self.__location_con_commit,
                                     self.__link_con_commit)

        try:
            self.cur_add_commit.execute(self.__cursor_query_commit, self.__cursor_values_commit)
            mydatabase.commit()
            messagebox.showinfo('Updated', 'The database has been updated')
        except:
            messagebox.showinfo('Error', 'An error occured. The database has not been updated')

        ## Bruk cursor, hent konferanser
        self.cur_add_commit.execute('''SELECT *
                                       FROM Conference''')

        ## Tøm treeview før oppdatering
        self.parent=self.tree.get_children('Conferences')
        for row in self.parent:
            self.tree.delete(row)

        ## Tellebasert løkke for å oppdatere treeview med konferanser
        ## Opprett teller for å holde styr på indeks
        self.__count=0
        for row in self.cur_add_commit:
            self.__name=row[0]
            self.__field=row[1]
            self.__time=row[2]
            self.__location=row[3]
            self.__link=row[4]
            ## Insert består av navnet på directory/katalog, indeks for rad i katalogen, og verdiene som skal settes inn.
            ## Komma mellom verdiene indikerer ny kolonne.
            self.tree.insert('Conferences', self.__count, values=(self.__name, self.__field, self.__time, self.__location, self.__link))
            ## Oppdater telleren
            self.__count +=1

        ## Lukk cursor
        self.cur_add_commit.close()


    ## Metode for å endre en konferanse
    def conference_edit(self):
        ## Steng eventuelle andre toplevels
        try:
            self.toplevel.destroy()
        except:
            pass
        
        ## Opprett nytt vindu
        self.toplevel=Toplevel(self.root)
        ## '-topmost' sikrer at vinduet alltid ligger øverst
        self.toplevel.attributes('-topmost', 'true')
        self.toplevel.title('Edit conference')
        self.toplevel.configure(bg='light sky blue')

        ## Beskrivende labels
        self.lbl_highlight=Label(self.toplevel, bg='light sky blue',
                                 text='Please highlight an element from the table to edit')
        self.lbl_name=Label(self.toplevel, width=16, bg='light sky blue', text='Name*')
        self.lbl_field=Label(self.toplevel, bg='light sky blue', text='Field')
        self.lbl_time=Label(self.toplevel, bg='light sky blue', text='Date*') 
        self.lbl_location=Label(self.toplevel, bg='light sky blue', text='Location')
        self.lbl_link=Label(self.toplevel, bg='light sky blue', text='Link')
        self.lbl_explanation=Label(self.toplevel, bg='light sky blue', text='Fields marked with * are mandatory')

        self.lbl_highlight.grid(row=0, column=0, padx=8, pady=8, sticky=W)
        self.lbl_name.grid(row=1, column=0, padx=8, pady=8, sticky=W)
        self.lbl_field.grid(row=1, column=1, padx=8, pady=8, sticky=W)
        self.lbl_time.grid(row=1, column=2, padx=8, pady=8, sticky=W)
        self.lbl_location.grid(row=1, column=3, padx=8, pady=8, sticky=W)
        self.lbl_link.grid(row=1, column=4, padx=8, pady=8, sticky=W)
        self.lbl_explanation.grid(row=3, column=0, padx=8, pady=8, sticky=W)

        ## Entry widgets
        self.__name_var=StringVar()
        self.ent_name=Entry(self.toplevel, width=32, textvariable=self.__name_var)
        ## Tkinter har dessverre ingen date picker, derav en enkel entry widget.
        self.__time_var=StringVar()
        self.ent_time=Entry(self.toplevel, width=16, textvariable=self.__time_var)
        self.__location_var=StringVar()
        self.ent_location=Entry(self.toplevel, width=32, textvariable=self.__location_var)
        self.__link_var=StringVar()
        self.ent_link=Entry(self.toplevel, width=32, textvariable=self.__link_var)

        self.ent_name.grid(row=2, column=0, padx=8, pady=8, sticky=W)
        self.ent_time.grid(row=2, column=2, padx=8, pady=8, sticky=W)
        self.ent_location.grid(row=2, column=3, padx=8, pady=8, sticky=W)
        self.ent_link.grid(row=2, column=4, padx=8, pady=8, sticky=W)

        ## Combobox
        self.combo=ttk.Combobox(self.toplevel, width=32, state='readonly', values=['',
                                                                                   'Big data',
                                                                                   'Open data',
                                                                                   'Software engineering',
                                                                                   'software engineering education',
                                                                                   'HCI'])
        self.combo.grid(row=2, column=1, padx=8, pady=8, sticky=W)
        self.combo.current(0)

        ## Button for å lagre endringer
        self.btn_update=Button(self.toplevel, width=16, text='Edit', command=self.conference_edit_commit)
        self.btn_update.grid(row=2, column=5, padx=8, pady=8, sticky=W)

        ## Igangsett hovedløkken
        self.toplevel.mainloop()


    ## Metode for å oppdatere databasen med endret konferanse
    def conference_edit_commit(self):
        self.__cursor_conedit=mydatabase.cursor()
        self.__cursor_conupdate=mydatabase.cursor()

        ## Varabler som skal kunne stå tomme gis null-merke
        self.__field_con_commit=str('NULL')
        self.__location_con_commit=str('NULL')
        self.__link_con_commit=str('NULL')
        
        # Variabler som skal substitueres
        self.__dataname=str(self.__name_var.get())
        self.__datafield=str(self.combo.get())
        self.__datatime=str(self.__time_var.get())
        self.__datalocation=str(self.__location_var.get())
        self.__datalink=str(self.__link_var.get())

        self.__conposname=str(self.__name_treeview.get())
        self.__conpostime=str(self.__time_treeview.get())

        # Lager substitsjons variablene
        self.__coneditquery=(""" UPDATE Conference 
                                SET ConferenceName=%s, 
                                        ConferenceField=%s, 
                                        ConferenceTime=%s, 
                                    ConferenceLocation=%s, 
                                    Link=%s  
                                WHERE ConferenceName=%s AND ConferenceTime=%s """)
        self.__conEditnew=(self.__dataname, self.__datafield, self.__datatime, self.__datalocation, self.__datalink, self.__conposname, self.__conpostime)

        try:
            self.__cursor_conedit.execute(self.__coneditquery, self.__conEditnew)
            mydatabase.commit()
            messagebox.showinfo('Updated', 'The database has been updated')

        except:
            messagebox.showinfo('Error', 'An error occured. The database has not been updated')

        self.__cursor_conedit.close()

        ## Bruk cursor, hent prosjekter
        self.__cursor_conupdate.execute('''SELECT *
                                          FROM Conference''')

        ## Tøm treeview før oppdatering
        self.parent=self.tree.get_children('Conferences')
        for row in self.parent:
            self.tree.delete(row)

        ## Tellebasert løkke for å oppdatere treeview med konferanser
        ## Opprett teller for å holde styr på indeks
        self.__count=0
        for row in self.__cursor_conupdate:
            self.__name=row[0]
            self.__field=row[1]
            self.__time=row[2]
            self.__location=row[3]
            self.__link=row[4]
            ## Insert består av navnet på directory/katalog, indeks for rad i katalogen, og verdiene som skal settes inn.
            ## Komma mellom verdiene indikerer ny kolonne.
            self.tree.insert('Conferences', self.__count, values=(self.__name, self.__field, self.__time, self.__location, self.__link))
            ## Oppdater telleren
            self.__count +=1
            
        self.__cursor_conupdate.close()
        


    ## Metode for å slette konferanse
    def conference_confirm_delete(self):
        ## Steng eventuelle andre toplevels
        try:
            self.toplevel.destroy()
        except:
            pass
        
        ## Opprett nytt vindu
        self.toplevel=Toplevel(self.root)
        ## '-topmost' sikrer at vinduet alltid ligger øverst
        self.toplevel.attributes('-topmost', 'true')
        self.toplevel.title('Delete conference')
        self.toplevel.configure(bg='light sky blue')

        ## Beskrivende labels
        self.lbl_highlight=Label(self.toplevel, bg='light sky blue',
                                 text='Please highlight an element from the table to delete')
        self.lbl_confirm=Label(self.toplevel, bg='light sky blue', text='Are you sure you wish to remove this conference?')

        self.lbl_highlight.grid(row=0, column=0, padx=8, pady=8, sticky=W)
        self.lbl_confirm.grid(row=1, column=0, padx=8, pady=8, sticky=W)
        
        ## Info om valgt konferanse
        ## Variabler
        self.__name_treeview=StringVar()
        self.__time_treeview=StringVar()
        self.ent_name=Entry(self.toplevel, width=32, textvariable=self.__name_treeview, state='readonly')
        self.ent_time=Entry(self.toplevel, width=16, textvariable=self.__time_treeview, state='readonly')
        
        self.ent_name.grid(row=2, column=0, padx=8, pady=8, sticky=W)
        self.ent_time.grid(row=2, column=1, padx=8, pady=8, sticky=W)

        ## Buttons
        self.btn_delete=Button(self.toplevel, width=16, text='Delete', command=self.conference_delete)
        self.btn_delete.grid(row=3, column=0, padx=8, pady=8, sticky=W)

        ## Igangsett hovedløkken
        self.toplevel.mainloop()

    ## Metode for å fjerne konferanse fra database
    def conference_delete(self):
        self.__name=self.__name_treeview.get()
        self.__time=self.__time_treeview.get()

        self.cursor=mydatabase.cursor()
        self.__cur_query=('''DELETE FROM Conference
                             WHERE ConferenceName=%s
                                 AND ConferenceTime=%s''')
        self.__cur_values=(self.__name, self.__time)

        try:
            self.cursor.execute(self.__cur_query, self.__cur_values)
            mydatabase.commit()
            messagebox.showinfo('Updated', 'The database has been updated')

        except:
            messagebox.showinfo('Error', 'An error occured. The database has not been updated')

        ## Bruk cursor, hent prosjekter
        self.cursor.execute('''SELECT *
                               FROM Conference''')

        ## Tøm treeview før oppdatering
        self.parent=self.tree.get_children('Conferences')
        for row in self.parent:
            self.tree.delete(row)

        ## Tellebasert løkke for å fylle treeview med konferanser
        ## Opprett teller for å holde styr på index
        self.__count=0
        for row in self.cursor:
            self.__name=row[0]
            self.__field=row[1]
            self.__time=row[2]
            self.__location=row[3]
            self.__link=row[4]
            ## Insert består av navnet på directory/katalog, indeks for rad i katalogen, og verdiene som skal settes inn.
            ## Komma mellom verdiene indikerer ny kolonne.
            self.tree.insert('Conferences', self.__count, values=(self.__name, self.__field, self.__time, self.__location, self.__link))
            ## Oppdater telleren
            self.__count +=1

        ## Lukk cursor
        self.cursor.close()


    ## Metode for å legge til prosjekt
    def project_add(self):
        ## Steng eventuelle andre toplevels
        try:
            self.toplevel.destroy()
        except:
            pass
        
        ## Opprett nytt vindu
        self.toplevel=Toplevel(self.root)
        ## '-topmost' sikrer at vinduet alltid ligger øverst
        self.toplevel.attributes('-topmost', 'true')
        self.toplevel.title('Add conference')
        self.toplevel.configure(bg='light sky blue')

        ## Beskrivende labels
        self.lbl_name_pro_add=Label(self.toplevel, width=16, bg='light sky blue', text='Name*')
        self.lbl_field_pro_add=Label(self.toplevel, bg='light sky blue', text='Field')
        self.lbl_time_pro_add=Label(self.toplevel, bg='light sky blue', text='Date*') 
        self.lbl_location_pro_add=Label(self.toplevel, bg='light sky blue', text='Location')
        self.lbl_explanation_pro_add=Label(self.toplevel, bg='light sky blue', text='Entries marked with * are mandatory')

        self.lbl_name_pro_add.grid(row=0, column=0, padx=8, pady=8, sticky=W)
        self.lbl_field_pro_add.grid(row=0, column=1, padx=8, pady=8, sticky=W)
        self.lbl_time_pro_add.grid(row=0, column=2, padx=8, pady=8, sticky=W)
        self.lbl_location_pro_add.grid(row=0, column=3, padx=8, pady=8, sticky=W)
        self.lbl_explanation_pro_add.grid(row=2, column=0, padx=8, pady=8, sticky=W)

        ## Entry widgets
        self.__name_var_pro_add=StringVar()
        self.ent_name_pro_add=Entry(self.toplevel, width=32, textvariable=self.__name_var_pro_add)
        ## Tkinter har dessverre ingen date picker, derav en enkel entry widget.
        self.__time_var_pro_add=StringVar()
        self.ent_time_pro_add=Entry(self.toplevel, width=16, textvariable=self.__time_var_pro_add)
        self.__location_var_pro_add=StringVar()
        self.ent_location_pro_add=Entry(self.toplevel, width=32, textvariable=self.__location_var_pro_add)

        self.ent_name_pro_add.grid(row=1, column=0, padx=8, pady=8, sticky=W)
        self.ent_time_pro_add.grid(row=1, column=2, padx=8, pady=8, sticky=W)
        self.ent_location_pro_add.grid(row=1, column=3, padx=8, pady=8, sticky=W)

        ## Combobox
        self.combo=ttk.Combobox(self.toplevel, width=32, state='readonly', values=['',
                                                                                                   'Big data',
                                                                                                   'Open data',
                                                                                                   'Software engineering',
                                                                                                   'software engineering education',
                                                                                                   'HCI'])
        self.combo.grid(row=1, column=1, padx=8, pady=8, sticky=W)
        self.combo.current(0)
        
                                                       

        ## Button for å lagre verdiene
        self.btn_update_pro_add=Button(self.toplevel, width=16, text='Add', command=self.project_add_commit)
        self.btn_update_pro_add.grid(row=1, column=5, padx=8, pady=8, sticky=W)

        ## Igangsett hovedløkken
        self.toplevel.mainloop()


    ## Metode for å oppdatere databasen med ett nytt prosjekt
    def project_add_commit(self):
        ## Opprett cursor for å lagre data
        self.cur_add_commit=mydatabase.cursor()

        ## Varabler som skal kunne stå tomme gis null-merke
        self.__field_con_commit=str('NULL')
        self.__location_con_commit=str('NULL')
        self.__link_con_commit=str('NULL')

        ## Variabler som skal sette i liste og executes
        self.__name_pro_commit=str(self.__name_var_pro_add.get())
        self.__field_pro_commit=str(self.combo.get())
        self.__time_pro_commit=str(self.__time_var_pro_add.get())
        self.__location_pro_commit=str(self.__location_var_pro_add.get())

        ## Query-del av execute
        self.__cursor_query_commit=('''INSERT INTO Project
                                       (ProjectName, ProjectField, ProjectStart, ProjectLocation)
                                       VALUES(%s, %s, %s, %s)''')
        ## Value-del av execute
        self.__cursor_values_commit=(self.__name_pro_commit,
                                     self.__field_pro_commit,
                                     self.__time_pro_commit,
                                     self.__location_pro_commit)

        try:
            self.cur_add_commit.execute(self.__cursor_query_commit, self.__cursor_values_commit)
            mydatabase.commit()
            messagebox.showinfo('Updated', 'The database has been updated')
        except:
            messagebox.showinfo('Error', 'An error occured. The database has not been updated')

        ## Bruk cursor, hent prosjekter
        self.cur_add_commit.execute('''SELECT *
                                       FROM Project''')

        ## Tøm treeview før oppdatering
        self.parent=self.tree.get_children('Projects')
        for row in self.parent:
            self.tree.delete(row)

        ## Tellebasert løkke for å oppdatere treeview med prosjekter
        ## Opprett teller for å holde styr på indeks
        self.__count=0
        for row in self.cur_add_commit:
            self.__name=row[0]
            self.__field=row[1]
            self.__time=row[2]
            self.__location=row[3]
            ## Insert består av navnet på directory/katalog, indeks for rad i katalogen, og verdiene som skal settes inn.
            ## Komma mellom verdiene indikerer ny kolonne.
            self.tree.insert('Projects', self.__count, values=(self.__name, self.__field, self.__time, self.__location))
            ## Oppdater telleren
            self.__count +=1

        ## Lukk cursor
        self.cur_add_commit.close()


    ## Metode for å endre et prosjekt
    def project_edit(self):
        ## Steng eventuelle andre toplevels
        try:
            self.toplevel.destroy()
        except:
            pass
        
        ## Opprett nytt vindu
        self.toplevel=Toplevel(self.root)
        ## '-topmost' sikrer at vinduet alltid ligger øverst
        self.toplevel.attributes('-topmost', 'true')
        self.toplevel.title('Edit research project')
        self.toplevel.configure(bg='light sky blue')

        ## Beskrivende labels
        self.lbl_highlight=Label(self.toplevel, bg='light sky blue',
                                 text='Please highlight an element from the table to edit')
        self.lbl_name=Label(self.toplevel, width=16, bg='light sky blue', text='Name*')
        self.lbl_field=Label(self.toplevel, bg='light sky blue', text='Field')
        self.lbl_time=Label(self.toplevel, bg='light sky blue', text='Starting date*') 
        self.lbl_location=Label(self.toplevel, bg='light sky blue', text='Location')
        self.lbl_explanation=Label(self.toplevel, bg='light sky blue', text='Fields marked with * are mandatory')

        self.lbl_highlight.grid(row=0, column=0, padx=8, pady=8, sticky=W)
        self.lbl_name.grid(row=1, column=0, padx=8, pady=8, sticky=W)
        self.lbl_field.grid(row=1, column=1, padx=8, pady=8, sticky=W)
        self.lbl_time.grid(row=1, column=2, padx=8, pady=8, sticky=W)
        self.lbl_location.grid(row=1, column=3, padx=8, pady=8, sticky=W)
        self.lbl_explanation.grid(row=3, column=0, padx=8, pady=8, sticky=W)

        ## Entry widgets
        self.__name_var=StringVar()
        self.ent_name=Entry(self.toplevel, width=32, textvariable=self.__name_var)
        ## Tkinter har dessverre ingen date picker, derav en enkel entry widget.
        self.__time_var=StringVar()
        self.ent_time=Entry(self.toplevel, width=16, textvariable=self.__time_var)
        self.__location_var=StringVar()
        self.ent_location=Entry(self.toplevel, width=32, textvariable=self.__location_var)

        self.ent_name.grid(row=2, column=0, padx=8, pady=8, sticky=W)
        self.ent_time.grid(row=2, column=2, padx=8, pady=8, sticky=W)
        self.ent_location.grid(row=2, column=3, padx=8, pady=8, sticky=W)

        ## Combobox
        self.combo=ttk.Combobox(self.toplevel, width=32, state='readonly', values=['',
                                                                                   'Big data',
                                                                                   'Open data',
                                                                                   'Software engineering',
                                                                                   'software engineering education',
                                                                                   'HCI'])
        self.combo.grid(row=2, column=1, padx=8, pady=8, sticky=W)
        self.combo.current(0)
        self.combo.current(0)

        ## Button for å lagre endringer
        self.btn_update=Button(self.toplevel, width=16, text='Edit', command=self.project_edit_commit)
        self.btn_update.grid(row=2, column=4, padx=8, pady=8, sticky=W)

        ## Igangsett hovedløkken
        self.toplevel.mainloop()

    def project_edit_commit(self):
        self.__cursor_proedit=mydatabase.cursor()
        self.__cursor_proupdate=mydatabase.cursor()

        ## Varabler som skal kunne stå tomme gis null-merke
        self.__field_con_commit=str('NULL')
        self.__location_con_commit=str('NULL')
        self.__link_con_commit=str('NULL')
        
        # Variabler som skal substitueres
        self.__dataname=str(self.__name_var.get())
        self.__datafield=str(self.combo.get())
        self.__datatime=str(self.__time_var.get())
        self.__datalocation=str(self.__location_var.get())
        self.__proposname=str(self.__name_treeview.get())
        self.__proposstart=str(self.__time_treeview.get())
        
        # Lager substitsjons variablene
        self.__proeditquery=(""" UPDATE Project 
                                 SET ProjectName=%s, 
                                    ProjectField=%s, 
                                    ProjectStart=%s, 
                                    ProjectLocation=%s   
                                 WHERE ProjectName=%s AND ProjectStart=%s """)
        self.__proeditnew=(self.__dataname, self.__datafield, self.__datatime, self.__datalocation, self.__proposname, self.__proposstart)

        try:
            self.__cursor_proedit.execute(self.__proeditquery, self.__proeditnew)
            mydatabase.commit()
            messagebox.showinfo('Updated', 'The database has been updated')

        except:
            messagebox.showinfo('Error', 'An error occured. The database has not been updated')

        self.__cursor_proedit.close()
            

        ## Bruk cursor, hent prosjekter
        self.__cursor_proupdate.execute('''SELECT *
                                           FROM Project''')
        
        ## Sletter innholdet i 'Projects'
        self.__existing_parent = self.tree.get_children('Projects')
        for item in self.__existing_parent:
            self.tree.delete(item)

        ## Tellebasert løkke for å fylle treeview med prosjekter
        ## Opprett teller for å holde styr på index
        self.__count=0
        for row in self.__cursor_proupdate:
            self.__name=row[0]
            self.__field=row[1]
            self.__time=row[2]
            self.__location=row[3]
            ## Insert
            self.tree.insert('Projects', self.__count, values=(self.__name, self.__field, self.__time, self.__location))
            ## Oppdater telleren
            self.__count +=1
            
        self.__cursor_proupdate.close()


    ## Metode for å slette prosjekt
    def project_confirm_delete(self):
        ## Steng eventuelle andre toplevels
        try:
            self.toplevel.destroy()
        except:
            pass
        
        ## Opprett nytt vindu
        self.toplevel=Toplevel(self.root)
        ## '-topmost' sikrer at vinduet alltid ligger øverst
        self.toplevel.attributes('-topmost', 'true')
        self.toplevel.title('Delete conference')
        self.toplevel.configure(bg='light sky blue')

        ## Beskrivende labels
        self.lbl_highlight=Label(self.toplevel, bg='light sky blue',
                                 text='Please highlight an element from the table to delete')
        self.lbl_confirm=Label(self.toplevel, bg='light sky blue', text='Are you sure you wish to remove this project?')

        self.lbl_highlight.grid(row=0, column=0, padx=8, pady=8, sticky=W)
        self.lbl_confirm.grid(row=1, column=0, padx=8, pady=8, sticky=W)
        
        ## Info om valgt prosjekt
        ## Variabler
        self.__name_treeview=StringVar()
        self.__time_treeview=StringVar()
        self.ent_name=Entry(self.toplevel, width=32, textvariable=self.__name_treeview, state='readonly')
        self.ent_time=Entry(self.toplevel, width=16, textvariable=self.__time_treeview, state='readonly')
        
        self.ent_name.grid(row=2, column=0, padx=8, pady=8, sticky=W)
        self.ent_time.grid(row=2, column=1, padx=8, pady=8, sticky=W)

        ## Buttons
        self.btn_delete=Button(self.toplevel, width=16, text='Delete', command=self.project_delete)
        self.btn_delete.grid(row=3, column=0, padx=8, pady=8, sticky=W)

        ## Igangsett hovedløkken
        self.toplevel.mainloop()


    ## Metode for å fjerne prosjekt fra database
    def project_delete(self):
        self.__name=self.__name_treeview.get()
        self.__time=self.__time_treeview.get()

        self.cursor=mydatabase.cursor()
        self.__cur_query=('''DELETE FROM Project
                             WHERE ProjectName=%s
                                 AND ProjectStart=%s''')
        self.__cur_values=(self.__name, self.__time)

        try:
            self.cursor.execute(self.__cur_query, self.__cur_values)
            mydatabase.commit()
            messagebox.showinfo('Updated', 'The database has been updated')

        except:
            messagebox.showinfo('Error', 'An error occured. The database has not been updated')

        ## Bruk cursor, hent prosjekter
        self.cursor.execute('''SELECT *
                               FROM Project''')

        ## Tøm treeview før oppdatering
        self.parent=self.tree.children_get('Projects')
        for row in self.parent:
            self.tree.delete(row)

        ## Tellebasert løkke for å fylle treeview med prosjekter
        ## Opprett teller for å holde styr på indeks
        self.__count=0
        for row in self.cursor:
            self.__name=row[0]
            self.__field=row[1]
            self.__time=row[2]
            self.__location=row[3]
            ## Insert består av navnet på directory/katalog, indeks for rad i katalogen, og verdiene som skal settes inn.
            ## Komma mellom verdiene indikerer ny kolonne.
            self.tree.insert('Projects', self.__count, values=(self.__name, self.__field, self.__time, self.__location))
            ## Oppdater telleren
            self.__count +=1

        ## Lukk cursor
        self.cursor.close()


    ## Metode for å sende seleksjon av treeview
    def tree_select(self, event):
        try:
            self.__curItem=self.tree.selection()
            self.__tempdict=self.tree.item(self.__curItem)
            self.__templst=self.__tempdict.get('values')

            try:
                #Set'ere
                self.__name_var.set(str(self.__templst[0]))
                self.combo.set(str(self.__templst[1]))
                self.__time_var.set(str(self.__templst[2]))
                self.__location_var.set(str(self.__templst[3]))
                self.__link_var.set(str(self.__templst[4]))

            ## Finally sikrer at et delete-vindu mottar de to siste .set-erene
            finally:
                #Set'er commit variablene til edit/delete
                self.__name_treeview.set(str(self.__templst[0]))
                self.__time_treeview.set(str(self.__templst[2]))

        except:
            pass

        


    def callback(self, event):
        ## Variabel tildeles "indeks" for linje i treeview
        self.__select=self.tree.selection()
        ## Hent dictionary fra treeview
        self.__dictionary=self.tree.item(self.__select)
        ## Konverter dictionary til liste
        self.__list=self.__dictionary.get('values')

        webbrowser.open(self.__list[4])


## Koble mot database
mydatabase=mysql.connector.connect(host='localhost', port='3306', user='Researcher', passwd='password', db='ResearcherProfile')

## Opprett en instanse av klassen
gui=MyGUI()

mydatabase.close()
