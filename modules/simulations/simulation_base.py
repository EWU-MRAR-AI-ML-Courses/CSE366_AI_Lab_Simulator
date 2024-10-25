# modules/simulations/simulation_base.py

import pygame

class SimulationBase:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        """Main loop of the simulation."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)  # Adjust the frame rate as needed

    def handle_events(self):
        """Handle user input and system events."""
        raise NotImplementedError("Subclasses should implement this method.")

    def update(self):
        """Update the simulation state."""
        raise NotImplementedError("Subclasses should implement this method.")

    def draw(self):
        """Draw the simulation elements on the screen."""
        raise NotImplementedError("Subclasses should implement this method.")

    def quit(self):
        """Exit the simulation."""
        self.running = False
