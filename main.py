# Standard library imports
# import os

# Set environment variable for Kivy audio backend before importing Kivy modules
# This helps prevent potential conflicts with default backends
# os.environ["KIVY_AUDIO"] = "sdl2"

# Kivy framework imports
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

# Import ScreenManager, Screen, and specific transition types
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, CardTransition
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.animation import Animation

# --- Configuration for Window Size and Aspect Ratio ---

initial_width = 400
initial_height = 600
aspect_ratio = initial_width / initial_height

# Optional: Set a background clear color if desired (currently commented out)
# Window.clearcolor = (0.9, 0.9, 0.9, 1)

# Define minimum window sizes to prevent excessive shrinking
Window.minimum_width = initial_width / 1.7
Window.minimum_height = initial_height / 1.7

# Set the initial dimensions of the application window
Window.size = (initial_width, initial_height)


def enforce_aspect_ratio(window_instance, width, height):
    """
    Dynamically adjusts window size to maintain a constant aspect ratio (4:6).

    This function is bound to the Kivy window's on_resize event. It calculates
    whether the current window size is too wide or too tall relative to the
    target aspect ratio and resizes the appropriate dimension (width or height)
    to enforce the constraint.
    """
    if width / height > aspect_ratio:
        # If the current aspect ratio is wider than desired, adjust width
        Window.size = (int(height * aspect_ratio), height)
    elif width / height < aspect_ratio:
        # If the current aspect ratio is taller than desired, adjust height
        Window.size = (width, int(width / aspect_ratio))

    # Returning True prevents Kivy's default resize behavior from overriding this logic
    return True


# Bind the custom aspect ratio enforcement function to the window resize event
Window.bind(on_resize=enforce_aspect_ratio)

# --- Screen Definitions ---


class LoginScreen(Screen):
    """
    Represents the initial screen where users input credentials.
    It handles input validation and navigation to the main menu screen.
    """

    def on_button_press(self):
        """
        Handles the logic when the 'Login' button is pressed in the KV file.

        Validates user input. If valid, it stores the username in the App
        instance and switches the screen manager's current screen to 'main_menu'.
        If invalid (empty username), an error message is displayed.
        """
        user_input_widget = self.ids.user_input
        output_label_widget = (
            self.ids.output_label
        )  # Note: This widget appears unused in the current logic
        error_label = self.ids.validation_label_error
        user_text = user_input_widget.text

        app_instance = App.get_running_app()
        app_instance.user_name = user_text

        if user_text:
            # Input is valid: hide error, clear inputs, and navigate
            error_label.opacity = 0
            self.ids.user_input.text = ""
            self.ids.phone_input.text = ""  # Clears the phone input field as well
            # Configure the transition direction for the *next* screen change
            self.manager.transition.direction = "right"
            self.manager.current = "main_menu"
        else:
            # Input is invalid (empty): show the validation error message
            error_label.opacity = 1
            # Optional: self.play_audio() might have been intended here


class FirstScreen(Screen):
    """
    The main menu screen displayed after successful login.
    It manages the background music playback and volume control functionality.
    """

    def on_enter(self):
        """
        Executed automatically by Kivy every time this screen becomes visible.
        Sets the welcome label text and initiates background music playback.
        """
        user_name = App.get_running_app().user_name or "Guest"
        # Format the welcome string with padding/centering
        welcome_string = f"{user_name.upper()}!"
        welcome_label = self.ids.welcome_label
        self.ids.welcome_label.text = welcome_string
        # --- Animation Logic for a Bouncy Entrance ---

        # 1. Store the final resting Y position
        # final_y_pos = welcome_label.y
        final_center_x_pos = Window.width / 2.0

        # 2. Start the widget much further down and invisible
        welcome_label.center_x = -Window.width / 2.0
        # welcome_label.y = final_y_pos - 100  # Start 300 pixels lower than final spot
        welcome_label.opacity = 0

        # 3. Define a "bouncy" animation
        # Use t='out_bounce' or t='in_elastic' for a more active feel
        anim = Animation(
            # top=final_top_pos,  # Animate to the top position we defined
            center_x=final_center_x_pos,  # Animate to the center of the screen
            opacity=1,  # Animate to fully visible
            duration=0.5,  # A slightly longer duration emphasizes the bounce
            t="out_cubic",  # The transition type is the key to the 'active' feel
        )

        # 4. Start the animation on the widget
        anim.start(welcome_label)
        # Start the background music when entering the main menu
        app_sound = App.get_running_app().background_sound
        if app_sound:
            app_sound.loop = True  # Set the music to loop continuously
            app_sound.play()
            # Set initial volume based on the slider's default value (assuming 50 max 100 in KV)
            initial_volume_value = self.ids.volume_slider.value / 100.0
            app_sound.volume = initial_volume_value
            print(f"Music started at volume: {app_sound.volume}")

    def set_volume(self, value):
        """
        Updates the volume of the background music based on the slider's value.

        Called by the Kivy Slider's on_value event defined in the KV file.
        Note: Kivy Sound volume expects a 0.0-1.0 float range, while the KV slider
        is assumed to have a default range (e.g., 0-100). This function scales the input.
        """
        app_sound = App.get_running_app().background_sound
        if app_sound:
            # Convert the slider's 0-100 value to the sound's 0.0-1.0 range
            app_sound.volume = value / 100.0

    def go_back_to_login(self):
        """
        Navigates back to the 'login' screen and stops the background music.

        This function is called by a button press event defined in the KV file.
        """
        # Set the transition direction for the *backward* navigation
        self.manager.transition.direction = "left"
        self.manager.current = "login"
        self.ids.welcome_label.text = ""
        # Stop the music when leaving the main menu screen
        app_sound = App.get_running_app().background_sound
        if app_sound:
            app_sound.stop()


# --- Main Application Class ---


class SimpleApp(App):
    """
    The main Kivy application class.

    It serves as a central hub for application data (like user_name and
    background_sound) and defines how the application structure (ScreenManager)
    is built. Kivy automatically loads 'simple.kv' when this class runs.
    """

    user_name = ""  # Shared variable to pass data between different screens/widgets
    background_sound = None  # Placeholder for the SoundLoader object

    def build(self):
        """
        Constructs the application's root widget tree (the ScreenManager).
        This method is required by the Kivy App lifecycle.
        """
        # Load the sound file reliably when the App object is fully initialized
        self.background_sound = SoundLoader.load("t5.mp3")
        if not self.background_sound:
            print("Error in App.build(): Audio file 't5.mp3' not found or unsupported.")
            # Optionally handle error: maybe load a default sound or disable sound functionality
        # Set up a ScreenManager with a custom transition type and duration
        sm = ScreenManager(transition=CardTransition(duration=0.4, mode="push"))

        # Add the defined screens to the manager, using unique names for navigation
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(FirstScreen(name="main_menu"))

        return sm


# --- Application Entry Point ---

if __name__ == "__main__":
    # Standard Python entry point to run the Kivy application loop
    SimpleApp().run()
