import ball
import my_event
import turtle
import random
import heapq
import paddle

class BouncingSimulator:
    def __init__(self, num_balls):
        self.num_balls = num_balls
        self.ball_list = []
        self.t = 0.0
        self.pq = []
        self.HZ = 4
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        print(self.canvas_width, self.canvas_height)

        ball_radius = 0.05 * self.canvas_width
        for i in range(self.num_balls):
            x = -self.canvas_width + (i+1)*(2*self.canvas_width/(self.num_balls+1))
            y = 0.0
            vx = 10*random.uniform(-1.0, 1.0)
            vy = 10*random.uniform(-1.0, 1.0)
            ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.ball_list.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color, i))
        
        self.tim = turtle.Turtle()
        self.tim.showturtle()
        self.tim.penup()
        self.tim.goto(0, 100)
        self.tim.pendown()

        tom = turtle.Turtle()
        self.my_paddle = paddle.Paddle(150, 50, (255, 0, 0), tom)
        self.my_paddle.set_location([100, -100])

        self.screen = turtle.Screen()

    # updates priority queue with all new events for a_ball
    def __predict(self, a_ball):
        if a_ball is None:
            return

        # particle-particle collisions
        for i in range(len(self.ball_list)):
            dt = a_ball.time_to_hit(self.ball_list[i])
            # insert this event into pq
            heapq.heappush(self.pq, my_event.Event(self.t + dt, a_ball, self.ball_list[i]))
        
        # particle-wall collisions
        dtX = a_ball.time_to_hit_vertical_wall()
        dtY = a_ball.time_to_hit_horizontal_wall()
        heapq.heappush(self.pq, my_event.Event(self.t + dtX, a_ball, None))
        heapq.heappush(self.pq, my_event.Event(self.t + dtY, None, a_ball))
    
    def __draw_border(self):
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(10)
        turtle.pendown()
        turtle.color((0, 0, 0))   
        for i in range(2):
            turtle.forward(2*self.canvas_width)
            turtle.left(90)
            turtle.forward(2*self.canvas_height)
            turtle.left(90)

    def __redraw(self):
        turtle.clear()
        self.my_paddle.clear()
        self.__draw_border()
        self.my_paddle.draw()
        for i in range(len(self.ball_list)):
            self.ball_list[i].draw()
        turtle.update()
        heapq.heappush(self.pq, my_event.Event(self.t + 1.0/self.HZ, None, None))

    # begin: event handlers
    def up(self):
        self.tim.setheading(90)
        self.tim.forward(10)

    def down(self):
        self.tim.setheading(270)
        self.tim.forward(10)

    def left(self):
        self.tim.setheading(180)
        self.tim.forward(10)

    def right(self):
        self.tim.setheading(0)
        self.tim.forward(10)

    def move_left(self):
        self.my_paddle.set_location([self.my_paddle.location[0] - 40, self.my_paddle.location[1]])

    def move_right(self):
        self.my_paddle.set_location([self.my_paddle.location[0] + 40, self.my_paddle.location[1]])
    
    # end: event handlers

    def run(self):
        # initialize pq with collision events and redraw event
        for i in range(len(self.ball_list)):
            self.__predict(self.ball_list[i])
        heapq.heappush(self.pq, my_event.Event(0, None, None))

        # begin: listening to keyboard events
        self.screen.listen()
        self.screen.onkey(self.up, "Up")
        self.screen.onkey(self.down, "Down")
        self.screen.onkey(self.left, "Left")
        self.screen.onkey(self.right, "Right")
        self.screen.onkey(self.move_left, "a")
        self.screen.onkey(self.move_right, "d")
        # end: listening to keyboard events

        while (True):
            e = heapq.heappop(self.pq)
            if not e.is_valid():
                continue

            ball_a = e.a
            ball_b = e.b

            # update positions, and then simulation clock
            for i in range(len(self.ball_list)):
                self.ball_list[i].move(e.time - self.t)
            self.t = e.time

            if (ball_a is not None) and (ball_b is not None):
                ball_a.bounce_off(ball_b)
            elif (ball_a is not None) and (ball_b is None):
                ball_a.bounce_off_vertical_wall()
            elif (ball_a is None) and (ball_b is not None):
                ball_b.bounce_off_horizontal_wall()
            else:
                self.__redraw()
            
            self.__predict(ball_a)
            self.__predict(ball_b)


        # hold the window; close it by clicking the window close 'x' mark
        turtle.done()

# num_balls = int(input("Number of balls to simulate: "))
num_balls = 10
my_simulator = BouncingSimulator(num_balls)
my_simulator.run()
