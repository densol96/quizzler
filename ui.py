from tkinter import *
from quiz_brain import QuizBrain
import time

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        wnd = self.window
        wnd.title("Quizzler")
        wnd.resizable(0, 0)
        wnd.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = Label(text=f"Score: {self.quiz.score}", bg=THEME_COLOR, fg="white", font=("Arial", 15, "normal"))
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

        true_button_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_button_image, highlightthickness=0, border=0, command=self.right)
        self.true_button.grid(row=2, column=0)

        false_button_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_button_image, highlightthickness=0, border=0, command=self.wrong)
        self.false_button.grid(row=2, column=1)
        

        wnd.update()
        h = wnd.winfo_height()
        w = wnd.winfo_width()

        print(f"Width: {w}, Height: {h}")
        
        wnd.mainloop()
    
    def get_next_question(self):
        self.canvas.config(bg="white")
        quiz_question_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=quiz_question_text)
        self.score_label.config(text=f"Score: {self.quiz.score}")
    
    def right(self):
        boolean_check = self.quiz.check_answer("True")
        self.feedback(boolean_check)
        
    def wrong(self):
        boolean_check = self.quiz.check_answer("False")
        self.feedback(boolean_check)
        
    def feedback(self, boolean_type):
        if boolean_type:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        
        self.window.after(1000, self.get_next_question)
