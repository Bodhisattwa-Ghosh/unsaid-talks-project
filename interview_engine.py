import json
from scorer import score_answer

with open("questions.json") as f:
    QUESTIONS = json.load(f)

TIME_LIMITS = {"Easy": 60, "Medium": 90, "Hard": 120}

class InterviewEngine:
    def __init__(self, skills):
        self.skills = skills
        self.current_difficulty = "Easy"
        self.question_count = 0
        self.scores = []
        self.terminated = False

    def get_question(self):
        skill = self.skills[self.question_count % len(self.skills)]
        question = QUESTIONS[skill][self.current_difficulty][0]
        self.current_skill = skill
        return question, TIME_LIMITS[self.current_difficulty]

    def evaluate(self, answer, time_taken):
        ideal = "Ideal answer for evaluation"
        max_time = TIME_LIMITS[self.current_difficulty]
        score = score_answer(answer, ideal, time_taken, max_time)

        self.scores.append(score)
        self.question_count += 1

        # Adaptive difficulty
        if score > 75:
            self.current_difficulty = "Medium" if self.current_difficulty == "Easy" else "Hard"
        elif score < 40:
            self.current_difficulty = "Easy"

        # Early termination
        if len(self.scores) >= 3 and sum(self.scores[-3:]) / 3 < 35:
            self.terminated = True

        return score

    def final_score(self):
        avg = sum(self.scores) / len(self.scores)
        return round(avg, 2)