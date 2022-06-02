aybio - ARTIFICIAL LIFE SIM

MORE INFORMATION AT: https://drive.google.com/file/d/1sqmgZEO1A9cCkoR4CbeYUBjDPnc4PhDZ/view?usp=sharing


The basic idea behind this project is more-niche version of RL-agent frameworks such as 
OpenAI's Gym (more like Deepmind's Lab). I intend to learn plenty more about AI than I already know,
as well as relevant hardware stacks (GPUs in particular, probably not going to end up looking into TPUs or NPUs). 

Of course, this isn't another toy project, I'm going to make it as performant and well written as I can overtime.

The entire stack aims to adhere to the following design principles:
 - Performance - it should do everything it possible can to be as performant as possible without
   interfering without getting in the way of adhereing to the other principles
 - Simplicity - it should be easy for one to put together how everything works
 - Minimal Dependendence - shouldn't depend on dozens of different libraries to do dozens of 
   different things.
 - ~~Desktop-hardware platform agnosticity - should be able perform parallel computations on 
   both NVIDIA and AMD's GPUs --- think more about this later, might end up using 
   wgpu to make this happen.~~ -- GOING TO WRITE OPENCL KERNEL PROGRAMS FOR THIS.

I am thinking of writing the backend as an ECS-like system:

- Environment - the backend
   - A world 
     - Has:
       - Rules
   - An agent(s)
     - Has a "brain"       
     - Can perform "actions"
     - Has to "perform well" in the "world"


JUNK (This is not indented to be readable for anyone else but me, but I put it here cos y not):
  Brainstorming - What exactly do I want to make?:
  - A player-agent-environment interaction-based game - more exploration than exploitation for the agent to do?
  - A more advanced version of Conway's Game of Life - food, random events, player-populus interaction, etc.
  - An aLife engine - recreating biological phenoma algorithmically.
  - micro-AI-based RTS game (units are intelligent).
  - Player vs. Artificially Intelligent Hostiles.
  - CURRENT PROTOTYPE IDEA: aLife simulator - 2D agents with custom genome coding (what kind of genomes? - t.b.d)

  Questions and what not - these may seem all over the place, so please excuse the lack of organization:
    - What governs the way life behaves?
      - Fitness Functions - scoring based on how agents meet an objective
        - Weighting different fitness functions (minor objectives), which are tuned to follow certain major objectives over time.
        It would be interesting to implement functions that manipulate an agent's desires - exploration vs. exploitation ?
    - How does life adapt (physically) to its environment, how can we emulate certain physical processes, and do so that we see extremely complex
    emergent behaviour (i.e communication, altruism, etc.)

    - Ideas for certain mechanisms:
      - Populate world with different sources of energy, each with its own way of being harnessed.
      The agents should eventually learn to harness these sources of energy for survival, with the help
      of mutation.
      - A toy simulation of abiogenesis?

  Research - Algorithms, theory, previous implementations and works: 
    - NEAT: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.18.4591&rank=1&q=NEAT&osm=&ossid=
    - Polyworld: http://shinyverse.org/larryy/Polyworld.html
    - Creatures game franchise
    - Automatic Goal Generation: https://arxiv.org/pdf/1705.06366.pdf
    - Muzero...

    General TODOs:
      - Look into emergent communication between RL agents.

    

