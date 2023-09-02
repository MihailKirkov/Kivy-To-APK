from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.uix.textinput import TextInput
import matplotlib.pyplot as plt
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from shutil import copyfileobj
import time
import sys
from pyicloud import PyiCloudService
import shutil
#
import os
from os import path
from zipfile import ZipFile
from shutil import copyfileobj
from bokeh.plotting import figure, output_file, show
from kivy.graphics import Color, Rectangle

patient_files = []
inattention_values = []
hyperactivity_values = []
impulsivity_values = []
emotional_dysregulation_values = []
executive_sequencing_values = []
executive_organization_values = []
medication_names = []
medication_doses = []
score_values = []
dates = []


QUESTIONS_LIST = [
    "1. At home, work, or school, I find my mind\nwandering from tasks that are \nuninteresting or difficult.",
    "2. I find it difficult to read written material\nunless it is very interesting or very easy.",
    "3. Especially in groups, I find it hard to\nstay focused on what is being\nsaid in conversations.",
    "4. I have a quick temper...a short fuse",
    "5. I am irritable, and get upset\nby minor annoyances",
    "6. I say things without thinking, and\nlater regret having said them.",
    "7. I make quick decisions without thinking\nenough about their possible bad results",
    "8. My relationships with people are made\ndifficult by my tendency to\ntalk first and think later.",
    "9. My moods have highs and lows.",
    "10. I have trouble planning in what order\nto do a series of tasks or activities.",
    "11. I easily become upset.",
    "12. I seem to be thin skinned\nand many things upset me. ",
    "13. I almost always am on the go.",
    "14. I am more comfortable when moving\nthan when sitting still.",
    "15. In conversations, I start to answer\nquestions before the questions\nhave been fully asked.",
    "16. I usually work on more than one\nproject at a time, and fail\nto finish many of them.",
    '17. There is a lot of "static"\nor "chatter" in my head.',
    "18. Even when sitting quietly, I am\nusually moving my hands or feet.",
    "19. In group activities it is hard\n for me to wait my turn.",
    "20. My mind gets so cluttered that\nit is hard for it to function",
    "21. My thoughts bounce around as if\nmy mind is a pinball machine.",
    "22. My brain feels as if it is a television\nset with all the channels going at once.",
    "23. I am unable to stop daydreaming.",
    "24. I am distressed by disorganization.",
    
]


class ChildApp(BoxLayout):
    def __init__(self, question_count, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.question_count = question_count

        self.inattention = 0
        self.hyperactivity = 0
        self.impulsivity = 0
        self.emotional_dysregulation = 0
        self.executive_sequencing = 0
        self.executive_organization = 0
        
        self.iCloudAcc(1)
    
    def update_button(self, index):
        self.clear_widgets()  # Clear existing widgets
        with self.canvas.before:
            Color(0.53, 0.81, 0.98, 1)  # RGB values for light blue
            self.rect = Rectangle(size=(self.width, self.height))
        

        # First Row: Text
        question = Label(text = QUESTIONS_LIST[self.question_count], halign="center",  valign="middle", color = (0,0,0,1))
        self.add_widget(question)


        # Second Row: 6 Buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1))
        button_layout.pos_hint = {'center_x': 0.5}

        button_texts = ['not\nat\nall', 'just\na\nlittle', 'somewhat', 'moderately', 'quite\na\nlot', 'very\nmuch']
        for i in range(6):
            # Calculate color gradient from red to green
            red_value = 1 - i / (6 - 1)
            green_value = i / (6 - 1)
            
            color = (green_value, red_value, 0, 1)
            
            button = Button(text=button_texts[i], background_color=color, color=get_color_from_hex('#FFFFFF'))
            button.bind(on_release=lambda instance, num = i: self.change_question(num, 1))
            button_layout.add_widget(button)

        
        self.add_widget(button_layout)        
        
    
    def change_question(self, num, index):
        

        if self.question_count == 23 : 
            self.executive_organization += num
            self.clear_widgets()
            self.print_results(1)

        else :
            if self.question_count in [0, 1, 2, 16, 19, 20, 21, 22]:
                self.inattention += num
            elif self.question_count in [12, 13, 17]:
                self.hyperactivity += num
            elif self.question_count in [5, 6, 7, 14, 18]:
                self.impulsivity += num
            elif self.question_count in [3, 4, 8, 10, 11]:
                self.emotional_dysregulation += num
            elif self.question_count in [9, 15]:
                self.executive_sequencing += num
            
            self.question_count = self.question_count+1
            self.update_button(1)
                    

    def patient_name(self, index):
        self.clear_widgets()
        self.api = PyiCloudService(self.cloud_user.text, self.cloud_pass.text)

        self.first_name = TextInput(hint_text="Enter Patient's First Name", multiline = False)
        self.add_widget(self.first_name)

        self.last_name = TextInput(hint_text="Enter Patient's Last Name", multiline = False)
        self.add_widget(self.last_name)

        self.gender = TextInput(hint_text = "Enter Patient's Gender", multiline = False)
        self.add_widget(self.gender)

        self.birth = TextInput(hint_text = "Enter Patient's Birth Date (YYYY-MM-DD)", multiline = False)
        self.add_widget(self.birth)

        self.date_input = TextInput(hint_text="Enter today's date (YYYY-MM-DD)", multiline=False)
        self.add_widget(self.date_input)

        self.medication_name = TextInput(hint_text = "Enter medication's name", multiline = False)
        self.add_widget(self.medication_name)

        self.medication_dose = TextInput(hint_text = "Enter medication's dose", multiline = False)
        self.add_widget(self.medication_dose)

        

        button = Button(text='Start Questionnaire', on_release = self.update_button)
        self.add_widget(button)


    def iCloudAcc(self,index):
        self.cloud_user = TextInput(hint_text="Enter your Apple ID for iCloud", multiline = False)
        self.add_widget(self.cloud_user)

        self.cloud_pass = TextInput(hint_text="Enter the password", multiline = False)
        self.add_widget(self.cloud_pass)

        button = Button(text='Next Page ( Patient Name, etc.)', on_release = self.patient_name)
        self.add_widget(button)
    

    def print_results(self, index):
        self.clear_widgets()
        self.score = self.inattention + self.hyperactivity + self.impulsivity + self.emotional_dysregulation + self.executive_sequencing + self.executive_organization

        button = Button(text='Upload to iCloud & Show Results', size_hint = (0.5,0.2), pos_hint = {'center_x': 0.5}, on_release = self.uploading)
        self.add_widget(button)

        

    def uploading(self, index): # upload saved data to iCloud as .txt
        text = f"inattenion:{self.inattention}\nhyperactivity:{self.hyperactivity}\nimpulsivity:{self.impulsivity}\nemotional_dysregulation:{self.emotional_dysregulation}\nexecutive_sequencing:{self.executive_sequencing}\nexecutive_organization:{self.executive_organization}\nmedication_name:{self.medication_name.text}\nmedication_dose:{self.medication_dose.text}\nscore:{self.score}\ngender:{self.gender}\nbirthday:{self.birth}"
        text_file_name = self.first_name.text + self.last_name.text + '_' + self.date_input.text + '.txt'

        self.clear_widgets()
        
        with open(text_file_name, 'w') as file: # write text into text file
            file.write(text)
        
        with open(text_file_name, 'rb') as file_in: # upload text file
            self.api.drive.upload(file_in)

        os.remove(text_file_name) # remove text file from local

        
        lines = text.strip().split('\n')

        dates.append('today')
        inattention_values.append (int(lines[0].split(':')[1]))
        hyperactivity_values.append (int(lines[1].split(':')[1]))
        impulsivity_values.append (int(lines[2].split(':')[1]))
        emotional_dysregulation_values.append (int(lines[3].split(':')[1]))
        executive_sequencing_values.append (int(lines[4].split(':')[1]))
        executive_organization_values.append (int(lines[5].split(':')[1]))
        medication_names.append(lines[6].split(':')[1])
        medication_doses.append(lines[7].split(':')[1])
        score_values.append(self.score)

        self.ImageSwapping(1)

    def ImageSwapping(self,index):
        

        name = self.first_name.text + self.last_name.text
        for file in self.api.drive.dir(): # add all files we should get the data from
            if file.split("_", 1)[0] == name:
                patient_files.append(file)
        
        patient_files.sort()
        print (patient_files)
        for file in patient_files:
            lines = self.api.drive[file].open().content.decode()
            lines = lines.strip().split('\r\n')
            inattention_values.append (int(lines[0].split(':')[1]))
            hyperactivity_values.append (int(lines[1].split(':')[1]))
            impulsivity_values.append (int(lines[2].split(':')[1]))
            emotional_dysregulation_values.append (int(lines[3].split(':')[1]))
            executive_sequencing_values.append (int(lines[4].split(':')[1]))
            executive_organization_values.append (int(lines[5].split(':')[1]))
            medication_names.append(lines[6].split(':')[1])
            medication_doses.append(lines[7].split(':')[1])
            score_values.append(int(lines[8].split(':')[1]))
            dates.append(file.split("_", 1)[1].strip('.txt')[2:])


        
        inattention_values.append(inattention_values.pop(0))
        hyperactivity_values.append(hyperactivity_values.pop(0))
        impulsivity_values.append(impulsivity_values.pop(0))
        emotional_dysregulation_values.append(emotional_dysregulation_values.pop(0))
        executive_sequencing_values.append(executive_sequencing_values.pop(0))
        executive_organization_values.append(executive_organization_values.pop(0))
        score_values.append(score_values.pop(0))

        medication_names.append(medication_names.pop(0))
        medication_doses.append(medication_doses.pop(0))
        dates.append(dates.pop(0))
        
        self.score_canvas(1)

    def score_canvas (self, index):
        self.clear_widgets()
        fig, graph = plt.subplots()
        graph.set_title("Total Score")
        graph.set_ylim(0,120)
        for i,value in enumerate(score_values):
            bar = graph.bar(f'{dates[i]}', value)  # Create the bar
            height = bar[0].get_height()  # Get the height of the first bar in the group
            graph.annotate(f'{medication_names[i]}\n{medication_doses[i]}',
                xy=(bar[0].get_x() + bar[0].get_width() / 2, height),
                xytext=(0, -20),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

        canvas = FigureCanvasKivyAgg(fig)
        
        self.add_widget(canvas)

        button = Button(text='Previous', on_release = self.executive_organization_canvas)
        button2 = Button(text = 'Next', on_release = self.inattention_canvas)
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        button_layout.pos_hint = {'center_x': 0.5}
        button_layout.add_widget(button)
        button_layout.add_widget(button2)
        self.add_widget(button_layout)


    def inattention_canvas(self, index):
        self.clear_widgets()
        fig, graph = plt.subplots()
        graph.set_title("INATTENTION SCORE PROGRESS")
        graph.set_ylim(0,40)
        for i,value in enumerate(inattention_values):
            bar = graph.bar(f'{dates[i]}', value)  # Create the bar
            height = bar[0].get_height()  # Get the height of the first bar in the group
            graph.annotate(f'{medication_names[i]}\n{medication_doses[i]}',
                xy=(bar[0].get_x() + bar[0].get_width() / 2, height),
                xytext=(0, -20),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

        canvas = FigureCanvasKivyAgg(fig)
        
        self.add_widget(canvas)

        button = Button(text='Previous', on_release = self.score_canvas)
        button2 = Button(text = 'Next', on_release = self.hyperactivity_canvas)
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        button_layout.pos_hint = {'center_x': 0.5}
        button_layout.add_widget(button)
        button_layout.add_widget(button2)
        self.add_widget(button_layout)
    
    def hyperactivity_canvas(self, index):
        self.clear_widgets()
        fig, graph = plt.subplots()
        graph.set_title("HYPERACTIVITY SCORE PROGRESS")
        graph.set_ylim(0,15)
        
        for i,value in enumerate(hyperactivity_values):
            bar = graph.bar(f'{dates[i]}', value)
            height = bar[0].get_height()  # Get the height of the first bar in the group
            graph.annotate(f'{medication_names[i]}\n{medication_doses[i]}',
                xy=(bar[0].get_x() + bar[0].get_width() / 2, height),
                xytext=(0, -20),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

        canvas = FigureCanvasKivyAgg(fig)
        
        self.add_widget(canvas)

        button = Button(text='Previous', on_release = self.inattention_canvas)
        button2 = Button(text = 'Next', on_release = self.impulsivity_canvas)
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        button_layout.pos_hint = {'center_x': 0.5}
        button_layout.add_widget(button)
        button_layout.add_widget(button2)
        self.add_widget(button_layout)

    def impulsivity_canvas(self, index):
        self.clear_widgets()
        fig, graph = plt.subplots()
        graph.set_title("IMPULSIVITY SCORE PROGRESS")
        graph.set_ylim(0,25)
        for i, value in enumerate(impulsivity_values):
            bar = graph.bar(f'{dates[i]}', value)
            height = bar[0].get_height()  # Get the height of the first bar in the group
            graph.annotate(f'{medication_names[i]}\n{medication_doses[i]}',
                xy=(bar[0].get_x() + bar[0].get_width() / 2, height),
                xytext=(0, -20),  # -3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

        plt.tight_layout()

        canvas = FigureCanvasKivyAgg(fig)
        
        self.add_widget(canvas)

        button = Button(text='Previous', on_release = self.hyperactivity_canvas)
        button2 = Button(text = 'Next', on_release = self.emotional_dysregulation_canvas)
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        button_layout.pos_hint = {'center_x': 0.5}
        button_layout.add_widget(button)
        button_layout.add_widget(button2)
        self.add_widget(button_layout)
        
    def emotional_dysregulation_canvas(self, index):
        self.clear_widgets()
        fig, graph = plt.subplots()
        graph.set_title("EMOTIONAL DYSREGULATION SCORE PROGRESS")
        graph.set_ylim(0,25)
        for i,value in enumerate(emotional_dysregulation_values):
            bar = graph.bar(f'{dates[i]}', value)
            height = bar[0].get_height()  # Get the height of the first bar in the group
            graph.annotate(f'{medication_names[i]}\n{medication_doses[i]}',
                xy=(bar[0].get_x() + bar[0].get_width() / 2, height),
                xytext=(0, -20),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

        canvas = FigureCanvasKivyAgg(fig)
        
        self.add_widget(canvas)

        button = Button(text='Previous', on_release = self.impulsivity_canvas)
        button2 = Button(text = 'Next', on_release = self.executive_sequencing_canvas)
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        button_layout.pos_hint = {'center_x': 0.5}
        button_layout.add_widget(button)
        button_layout.add_widget(button2)
        self.add_widget(button_layout)

    def executive_sequencing_canvas(self, index):
        self.clear_widgets()
        fig, graph = plt.subplots()
        graph.set_title("EXECUTIVE SEQUENCING SCORE PROGRESS")
        graph.set_ylim(0,10)
        for i,value in enumerate(executive_sequencing_values):
            bar = graph.bar(f'{dates[i]}', value)
            height = bar[0].get_height()  # Get the height of the first bar in the group
            graph.annotate(f'{medication_names[i]}\n{medication_doses[i]}',
                xy=(bar[0].get_x() + bar[0].get_width() / 2, height),
                xytext=(0, -20),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

        canvas = FigureCanvasKivyAgg(fig)
        
        self.add_widget(canvas)

        button = Button(text='Previous', on_release = self.emotional_dysregulation_canvas)
        button2 = Button(text = 'Next', on_release = self.executive_organization_canvas)
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        button_layout.pos_hint = {'center_x': 0.5}
        button_layout.add_widget(button)
        button_layout.add_widget(button2)
        self.add_widget(button_layout)
        
    def executive_organization_canvas(self, index):
        self.clear_widgets()
        fig, graph = plt.subplots()
        graph.set_title("EXECUTIVE ORGANIZATION SCORE PROGRESS")
        graph.set_ylim(0,5)
        for i,value in enumerate(executive_organization_values):
            bar = graph.bar(f'{dates[i]}', value)
            height = bar[0].get_height()  # Get the height of the first bar in the group
            graph.annotate(f'{medication_names[i]}\n{medication_doses[i]}',
                xy=(bar[0].get_x() + bar[0].get_width() / 2, height),
                xytext=(0, -20),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

        canvas = FigureCanvasKivyAgg(fig)
        
        self.add_widget(canvas)

        button = Button(text='Previous', on_release = self.executive_sequencing_canvas)
        button2 = Button(text = 'Next', on_release = self.score_canvas)
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        button_layout.pos_hint = {'center_x': 0.5}
        button_layout.add_widget(button)
        button_layout.add_widget(button2)
        self.add_widget(button_layout)


class MyApp(App):
    def build(self):
        return ChildApp(question_count=0)

if __name__ == "__main__":
    MyApp().run()
