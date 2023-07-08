from tkinter import *
from tkinter import messagebox
from quiz_brain import QuizBrain
from question_model import Question
import time
import requests
THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz: QuizBrain):

        self.quiz = quiz
        self.counter = 0
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.geometry("340x516")
        self.window.config(bg=THEME_COLOR)
        self.window.resizable(0, 0)
        self.setup()
        self.window.mainloop()
    
    def setup(self):
        self.window.config(padx=15, pady=80)
        
        self.greeting = Label(text="Welcome to Quizler!", fg="white", bg=THEME_COLOR, font=("Arial", 20, "bold"))
        self.greeting.grid(row=0, column=0, columnspan=2)
        
        self.instruction = Label(text="Choose your setup", fg="white", bg=THEME_COLOR, font=("Arial", 15, "normal"))
        self.instruction.grid(row=1, column=0, columnspan=2)
        self.placeholder = Label(bg=THEME_COLOR, height=3)
        self.placeholder.grid(row=2, column=0, columnspan=2)
        
        self.number = Label(text="Number of questions:", fg="white", bg=THEME_COLOR, font=("Arial", 12, "normal"), height=2)
        self.number.grid(row=3, column=0, sticky="w")

        self.difficulty = Label(text="Difficulty:", fg="white", bg=THEME_COLOR, font=("Arial", 12, "normal"), height=2)
        self.difficulty.grid(row=4, column=0, sticky="w")
        
        self.category = Label(text="Category:", fg="white", bg=THEME_COLOR, font=("Arial", 12, "normal"), height=2)
        self.category.grid(row=5, column=0, sticky="w")


        self.number_dropdown = Spinbox(from_=0, to=10)
        self.number_dropdown.config(width=20)
        self.number_dropdown.grid(row=3, column=1)

        self.selected_difficulty = StringVar()
        self.selected_difficulty.set("---choose---")
        self.diffulty_dropdown = OptionMenu(self.window, self.selected_difficulty, "easy", "medium", "hard")
        self.diffulty_dropdown.config(width=15)
        self.diffulty_dropdown.grid(row=4, column=1, padx=20)

        self.selected_category = StringVar()
        self.selected_category.set("---choose---")
        options = ["General", "Computers", "Politics", "Animals", "Math"]
        self.category_dropdown = OptionMenu(self.window, self.selected_category, *options)
        self.category_dropdown.config(width=15)
        self.category_dropdown.grid(row=5, column=1, padx=20)

        self.button = Button(text="Submit", command=self.submit)
        self.button.config(width=20)
        self.button.grid(row=6, column=0, columnspan=2, pady=30)
    
    def submit(self):
        self.button.config(state="disabled")

        number = self.number_dropdown.get()
        difficulty = self.selected_difficulty.get()
        category = self.selected_category.get()

        if number == 0 or difficulty == "---choose---" or category == "---choose---":
            messagebox.showwarning(title="Warning!", message="You have left some field empty!")
            self.button.config(state="active")
        else:
            check = messagebox.askokcancel(title="Confirm the details", 
                                           message="These are the details entered:\n"
                                           f"Number of questions: {number}\n"
                                           f"Difficulty: {difficulty}\n"
                                            f"Category: {category}\n"
                                            "\nAre the details correct?")
        
            if check:
                if category == "General":
                    category = 9
                elif category == "Computers":
                    category = 18
                elif category == "Politics":
                    category = 24
                elif category == "Animals":
                    category = 27
                elif category == "Math":
                    category = 19

                parameters = {
                    "amount": number,
                    "category": category,
                    "difficulty": difficulty,
                    "type": "boolean"
                }

                self.quiz.question_list = self.api_request(parameters)
                self.destroy_setup()
                print(self.quiz.question_list)
                if len(self.quiz.question_list) == 0:
                    self.quiz.question_list = self.api_request()
                self.new(self.quiz)
            else:
                self.button.config(state="active")

    def api_request(self, parameters=None):

        api_endpoint = "https://opentdb.com/api.php"
        if parameters is not None:
            response = requests.get(url=api_endpoint, params=parameters)
        else:
            response = requests.get(url="https://opentdb.com/api.php?amount=10&type=boolean")

        response.raise_for_status()
        data = response.json()["results"]

        question_bank = []
        for question in data:
            question_text = question["question"]
            question_answer = question["correct_answer"]
            new_question = Question(question["question"], question["correct_answer"])
            question_bank.append(new_question)
        
        return question_bank

    def destroy_setup(self):
        self.greeting.destroy()
        self.instruction.destroy()
        self.placeholder.destroy()
        self.number.destroy()
        self.difficulty.destroy()
        self.category.destroy()
        self.number_dropdown.destroy()
        self.diffulty_dropdown.destroy()
        self.category_dropdown.destroy()
        self.button.destroy()
        

    def new(self, quiz_brain: QuizBrain):
        self.window.config(padx=20, pady=20)

        self.score_label = Label(text=f"Score: {self.quiz.score} / {len(self.quiz.question_list)}", bg=THEME_COLOR, fg="white", font=("Arial", 15, "normal"))
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, highlightthickness=0, bg="white")
        self.question_text = self.canvas.create_text(
            150, 
            125,
            width=280, 
            text="Some pretty long checking placeholder text..", 
            fill=THEME_COLOR, 
            font=("Arial", 20, "italic")
        )
        self.get_next_question()
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        self.true_button_image = PhotoImage(file="./images/true.png")
        self.true_button = Button(image=self.true_button_image, highlightthickness=0, border=0, command=self.right)
        self.true_button.grid(row=2, column=0)

        self.false_button_image = PhotoImage(file="./images/false.png")
        self.false_button = Button(image=self.false_button_image, highlightthickness=0, border=0, command=self.wrong)
        self.false_button.grid(row=2, column=1)
    
    def get_next_question(self):
        try:
            self.true_button.config(state="active")
            self.false_button.config(state="active")
        except:
            pass
        self.canvas.config(bg="white")
        self.score_label.config(text=f"Score: {self.quiz.score} / {len(self.quiz.question_list)}")
        if self.counter < len(self.quiz.question_list):
            quiz_question_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=quiz_question_text)
        else:
            self.canvas.itemconfig(self.question_text, text=f"Game Over\nYou scored: {self.quiz.score} / {len(self.quiz.question_list)}")
            self.true_button.destroy()
            self.false_button.destroy()
            self.reset_button = Button(text="Reset", command=self.reset)
            self.reset_button.config(width=20)
            self.reset_button.grid(row=2, column=0, columnspan=2, pady=10)

    
    def right(self):
        boolean_check = self.quiz.check_answer("True")
        self.feedback(boolean_check)
        
    def wrong(self):
        boolean_check = self.quiz.check_answer("False")
        self.feedback(boolean_check)
        
    def feedback(self, boolean_type):
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")
        self.counter += 1
        if boolean_type:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        

        self.window.after(1000, self.get_next_question)

    def reset(self):
        self.reset_button.config(state="disabled")
        self.counter = 0
        self.quiz.score = 0
        self.quiz.question_number = 0
        self.score_label.destroy()
        self.canvas.destroy()
        self.reset_button.destroy()
        self.setup()