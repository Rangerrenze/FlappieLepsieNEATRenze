import pygame
import neat
import sys
import os
import math
import random
import pygame as p
import visualize

loadCP = 60 #Laad vanaf dit checkpoint
checkpointing = False #Laad van aangegeven checkpoint
runGenerations = 2 #Aantel generation om te runnen




pygame.init()
clock = pygame.time.Clock()
WINDOW = (800,600)
pygame.display.set_caption("Flappylepsie")
DrawLines = True
screen =p.display.set_mode(WINDOW)
display = p.Surface(WINDOW)
p.font.init()
font = pygame.font.SysFont('Comic Sans MS', 25)

roof = pygame.Rect(0, 0, WINDOW[0], 10)
floor = pygame.Rect(0, WINDOW[1]-10, WINDOW[0], 10)



scrollSpeed = 5

generation = 0

totalScore = 0

class Flappy():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vertical_Speed = 0
        self.FlappySquare = p.Rect((self.x, self.y), (self.width, self.height))
        self.BaseClosestPipe = Pipes[0][0]
        self.score = 0
        self.pipescore = 0

    def update(self):
        self.x, self.y = self.FlappySquare.x, self.FlappySquare.y
        self.Movement()

    def draw(self):
        self.Color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        p.draw.rect(display, self.Color, self.FlappySquare)

    def flyUp(self):
        self.vertical_Speed = -5

    def Movement(self):
        self.FlappySquare.y +=self.vertical_Speed

        self.vertical_Speed += 0.2
        if self.vertical_Speed >= 4:
            self.vertical_Speed = 4

class pipes():
    def __init__(self, x, y, widht, height, scrollSpeed = 5):
        self.x = x
        self.y = y
        self.width = widht
        self.height = height
        self.scrollSPeed = scrollSpeed
        self.pipe = p.Rect(x, y, self.width, self.height)
    def update(self):
        self.x -=self.scrollSPeed
        self.pipe.x, self.pipe.y = self.x, self.y

    def draw(self):
        self.Color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        p.draw.rect(display, self.Color, self.pipe)

def getDistance(firstPos, secondPos):
    dx = firstPos[0] - secondPos[0]
    dy = firstPos[1] - secondPos[1]
    return math.sqrt(dx**2 + dy**2)

def removeFlappy(index):
    flappys.pop(index)
    ge.pop(index)
    nets.pop(index)

def draw():
    Color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    Color2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    Color3 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    display.fill('black')
    # p.draw.line(display, ('red'), (0, 0), (WINDOW[0], 0), 10)
    # p.draw.line(display, ('red'), (0, WINDOW[1]), (WINDOW[0], WINDOW[1]), 10)

    p.draw.rect(display, (Color2), floor)
    p.draw.rect(display, (Color3), roof)


    for flappy in flappys:
        flappy.draw()
        if DrawLines:
            p.draw.line(
                display,
                ('Red'),
                (flappy.FlappySquare.right, flappy.FlappySquare.centery),
                flappy.closestPipe[0].pipe.midbottom,
                2
            )

    for pipe in Pipes:
        pipe[0].draw()
        pipe[1].draw()


    bestscore = 0
    for flappy in flappys:
        if bestscore < flappy.score:
            bestscore = flappy.score
    totalScore = 0
    for flappy in flappys:
        if totalScore < flappy.pipescore:
            totalScore = flappy.pipescore


    textAlive = font.render(f'Flappys alive: {len(flappys)}', 1, 'white')
    generationsText = font.render(f'Generation: {generation}', 1, 'white')
    scoreText = font.render(f'Score: {bestscore}', 1, 'white')
    scoreText2 = font.render(f'Pipes: {totalScore}', 1, 'white')
    display.blit(textAlive, (5, WINDOW[1] - 40))
    display.blit(generationsText, (5, WINDOW[1] - 75))
    display.blit(scoreText, (5, WINDOW[1]-110))
    display.blit(scoreText2, (5, WINDOW[1]-145))
    screen.blit(display, (0, 0))
    p.display.update()



def main(genomes, config):
    global Pipes,flappys, nets, ge, generation
    PipeLen = WINDOW[1] - 150
    TopHeight = PipeLen/3 + random.randint(0,175)
    BottomHeight = PipeLen-TopHeight
    Pipes = [(pipes(WINDOW[0], 0, 30, TopHeight), pipes(WINDOW[0], WINDOW[1] - BottomHeight, 30, BottomHeight))]

    flappys = []
    nets =[]
    ge = []
    scrollSpeed = 5
    generation += 1

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        flappys.append(Flappy(100, 100, 40, 40))
        g.fitness = 0
        ge.append(g)

    run = True
    while run:
        clock.tick(60)
        for event in p.event.get():
            if event.type == p.QUIT:
                pygame.quit()
                sys.exit()
        if len(flappys) <= 0:
            break

        if len(Pipes) <= 1:
            # if Pipes[0].x < random.randint(300, WINDOW[0] - 200) + scrollSpeed:
            if Pipes[0][0].x < WINDOW[0]//2:
                PipeLen = WINDOW[1] - 150
                TopHeight = PipeLen/3 + random.randint(0, 175)
                BottomHeight = PipeLen - TopHeight
                Pipes.append((pipes(WINDOW[0], 0, 30, TopHeight, scrollSpeed), pipes(WINDOW[0], WINDOW[1] - BottomHeight, 30, BottomHeight, scrollSpeed)))

        for pipe in Pipes:
            pipe[0].update()
            pipe[1].update()
            if pipe[0].x < -100:
                Pipes.remove(pipe)
            for i, flappy in enumerate(flappys):
                flappy.update()
                if flappy.FlappySquare.colliderect(pipe[0].pipe) or flappy.FlappySquare.colliderect(pipe[1].pipe) or flappy.FlappySquare.colliderect(floor) or flappy.FlappySquare.colliderect(roof) or flappy.y > WINDOW[1]:
                    ge[i].fitness -= 3
                    removeFlappy(i)
        for i, flappy in enumerate(flappys):
            flappy.update()
            flappy.closestPipe = [pipe for pipe in Pipes if pipe[0].pipe.x > flappy.x - flappy.width][0]
            if flappy.closestPipe != flappy.BaseClosestPipe:
                ge[i].fitness += 1
                flappy.score += random.randint(0, 100)
                flappy.pipescore += 1
                if i == 0:
                    for pipe in Pipes:
                        pipe[0].scrollSPeed += 0.05
                        pipe[1].scrollSPeed += 0.05
                        scrollSpeed += 0.05

            pipeDist2 = 1
            pipeX2 = 1
            PipeHeight2 = 1
            if len(Pipes) > 1:
                pipeDist2 = getDistance((flappy.x, flappy.y), Pipes[1][0].pipe.midbottom)
                pipeX2 = Pipes[1][0].x
                PipeHeight2 = Pipes[1][0].height

            output = nets[i].activate(
                (
                    flappy.y,
                    getDistance((flappy.x, flappy.y), flappy.closestPipe[0].pipe.midbottom),
                    getDistance((flappy.x, flappy.y), flappy.closestPipe[1].pipe.midtop),
                    flappy.closestPipe[0].height,
                    flappy.closestPipe[1].y,
                    pipeDist2,
                    PipeHeight2,
                    len(Pipes)
                )
            )
            flappy.BaseClosestPipe = flappy.closestPipe
            ge[i].fitness += 0.5
            if output[0] > 0.5:
                flappy.flyUp()

        draw()

def run(config_path):
    print("test")
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    if checkpointing:
        tmpGens = loadCP - 1
        tmpname = 'neat-checkpoint-{0}'.format(tmpGens)

        p = neat.checkpoint.Checkpointer.restore_checkpoint(tmpname)
        generation = p.generation
    else:
        p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.checkpoint.Checkpointer(20,20))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, runGenerations)
    visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

    node_names = {-1: 'x', -2: 'dx', -3: 'theta', -4: 'dtheta', 0: 'control'}
    visualize.draw_net(config, winner, True, node_names=node_names)

    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward.gv")
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward-enabled.gv", show_disabled=False)
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)



if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
