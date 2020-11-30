from gym_duckietown.tasks.task_solution import TaskSolution
import numpy as np
import cv2


class DontCrushDuckieTaskSolution(TaskSolution):
    def __init__(self, generated_task):
        super().__init__(generated_task)

    def yellowRatio(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        '''yellow'''
        # Range for upper range
        yellow_lower = np.array([20, 100, 100])
        yellow_upper = np.array([30, 255, 255])
        mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

        yellow_ratio = (cv2.countNonZero(mask_yellow)) / (image.size / 3)

        return np.round(yellow_ratio * 100, 2)

    def solve(self):
        env = self.generated_task['env']
        #        actions = [[1, 0] for _ in range(42)]
        #        for action in actions:
        #            env.step(action)
        #            env.render()
        #            print(str(env.cur_pos) + " ::: " + str(target_coordinates))
        obs, _, _, _ = env.step([0, 0])
        img = cv2.cvtColor(np.ascontiguousarray(obs), cv2.COLOR_BGR2RGB)
        print('self.yellowRatio(obs) = ', self.yellowRatio(img))

        while self.yellowRatio(img) < 6.5:
            obs, reward, done, info = env.step([0.5, 0])
            #img = cv2.cvtColor(np.ascontiguousarray(obs), cv2.COLOR_BGR2RGB)
            img = obs
            print('self.yellowRatio(obs) = ', self.yellowRatio(img))
            env.render()

        for i in range(30):
            env.step([0, 0])
            env.render()