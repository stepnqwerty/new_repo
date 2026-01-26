import random
import time
import os
import math
import argparse
from PIL import Image
import requests
from io import BytesIO

class ASCIIArtGenerator:
    def __init__(self):
        # Define character sets for different styles
        self.charsets = {
            'standard': ' .:-=+*#%@',
            'simple': ' .oO0@',
            'blocks': ' ░▒▓█',
            'detailed': ' .\'`^",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$',
            'binary': ' 01',
            'dots': ' ·•●',
            'lines': ' ━┃┏┓┗┛┣┫┳┻╋'
        }
        
        self.colors = {
            'reset': '\033[0m',
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m'
        }
        
        self.current_charset = 'standard'
        self.current_color = 'white'
        self.width = 80
        self.height = 24
        self.animation_running = False
        
    def image_to_ascii(self, image_path, width=None, height=None, charset=None, color=None):
        """Convert an image to ASCII art"""
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        if charset is None:
            charset = self.current_charset
        if color is None:
            color = self.current_color
            
        # Load image
        if image_path.startswith('http'):
            response = requests.get(image_path)
            img = Image.open(BytesIO(response.content))
        else:
            img = Image.open(image_path)
            
        # Convert to grayscale and resize
        img = img.convert('L')
        img_ratio = img.height / img.width
        new_height = int(height * 0.5)  # Adjust for character aspect ratio
        img = img.resize((width, new_height))
        
        # Get pixel data
        pixels = img.getdata()
        
        # Map pixels to ASCII characters
        ascii_chars = []
        for pixel in pixels:
            # Normalize pixel value to charset index
            char_index = int(pixel / 255 * (len(charset) - 1))
            ascii_chars.append(charset[char_index])
            
        # Create ASCII art string
        ascii_art = ""
        for i in range(new_height):
            start = i * width
            end = start + width
            line = "".join(ascii_chars[start:end])
            ascii_art += f"{self.colors[color]}{line}{self.colors['reset']}\n"
            
        return ascii_art
    
    def text_to_ascii(self, text, style=None, color=None):
        """Convert text to ASCII art with different styles"""
        if style is None:
            style = 'standard'
        if color is None:
            color = self.current_color
            
        # Simple text to ASCII conversion with different styles
        if style == 'banner':
            return self.text_to_banner(text, color)
        elif style == 'block':
            return self.text_to_block(text, color)
        elif style == '3d':
            return self.text_to_3d(text, color)
        else:
            return f"{self.colors[color]}{text}{self.colors['reset']}"
    
    def text_to_banner(self, text, color):
        """Create banner-style ASCII text"""
        banner_chars = {
            'A': ["  ╔═╗  ", "  ╠═╣  ", "  ╩ ╩  "],
            'B': ["  ╔╗   ", "  ╠╩╗  ", "  ╚═╝  "],
            'C': ["  ╔═╗  ", "  ║    ", "  ╚═╝  "],
            'D': ["  ╔╦╗  ", "   ║║  ", "  ╚╝   "],
            'E': ["  ╔═╗  ", "  ╠═   ", "  ╚═╝  "],
            'F': ["  ╔═╗  ", "  ╠═   ", "  ╩    "],
            'G': ["  ╔═╗  ", "  ║ ╦  ", "  ╚═╝  "],
            'H': ["  ╦ ╦  ", "  ╠═╣  ", "  ╩ ╩  "],
            'I': ["  ╦    ", "  ║    ", "  ╩    "],
            'J': ["     ╦ ", "     ║ ", "  ╚═╝  "],
            'K': ["  ╦╔═  ", "  ╠╩╗  ", "  ╩ ╩  "],
            'L': ["  ╦    ", "  ║    ", "  ╚═╝  "],
            'M': ["  ╔╦╗  ", "  ║║║  ", "  ╩ ╩  "],
            'N': ["  ╔╗╔  ", "  ║║║  ", "  ╝╚╝  "],
            'O': ["  ╔═╗  ", "  ║ ║  ", "  ╚═╝  "],
            'P': ["  ╔═╗  ", "  ╠═╝  ", "  ╩    "],
            'Q': ["  ╔═╗  ", "  ║═╬╗ ", "  ╚═╝╚ "],
            'R': ["  ╔═╗  ", "  ╠╦╝  ", "  ╩╚═  "],
            'S': ["  ╔═╗  ", "  ╚═╗  ", "  ╚═╝  "],
            'T': ["  ╦═╗  ", "  ╠╦╝  ", "  ╩╚═  "],
            'U': ["  ╦ ╦  ", "  ║ ║  ", "  ╚═╝  "],
            'V': ["  ╦  ╦ ", "  ║  ║ ", "  ╚═╚╝ "],
            'W': ["  ╦ ╦  ", "  ║║║  ", "  ╚╩╝  "],
            'X': ["  ╦ ╦  ", "   ║   ", "  ╚═╝  "],
            'Y': ["  ╦ ╦  ", "   ║   ", "   ╩   "],
            'Z': ["  ╔═╗  ", "   ╔╝  ", "  ╚═╝  "],
            ' ': ["       ", "       ", "       "]
        }
        
        result = ["", "", ""]
        for char in text.upper():
            if char in banner_chars:
                for i in range(3):
                    result[i] += banner_chars[char][i]
        
        return f"{self.colors[color]}\n".join(result) + self.colors['reset']
    
    def text_to_block(self, text, color):
        """Create block-style ASCII text"""
        block_text = f"""
{self.colors[color]}
╔════════════════════════════════════════╗
║                                      ║
║  {text.center(36)}  ║
║                                      ║
╚════════════════════════════════════════╝
{self.colors['reset']}
"""
        return block_text
    
    def text_to_3d(self, text, color):
        """Create 3D-style ASCII text"""
        lines = []
        for i, char in enumerate(text):
            shadow = " " * i
            lines.append(f"{shadow}{self.colors[color]}{char}{self.colors['reset']}")
        return "\n".join(lines)
    
    def create_animation(self, frames, delay=0.1, loop=True):
        """Create and display an ASCII animation"""
        self.animation_running = True
        
        try:
            while self.animation_running:
                for frame in frames:
                    if not self.animation_running:
                        break
                    os.system('clear' if os.name == 'posix' else 'cls')
                    print(frame)
                    time.sleep(delay)
                if not loop:
                    break
        except KeyboardInterrupt:
            self.animation_running = False
    
    def stop_animation(self):
        """Stop the current animation"""
        self.animation_running = False
    
    def create_matrix_rain(self, width=80, height=24, duration=10):
        """Create a Matrix-style rain animation"""
        columns = [0] * width
        chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        
        end_time = time.time() + duration
        
        while time.time() < end_time and self.animation_running:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            # Create a new screen
            screen = []
            for _ in range(height):
                screen.append([' '] * width)
            
            # Add characters to screen
            for i in range(width):
                if columns[i] == 0 or random.random() < 0.05:
                    # Reset column or start new rain
                    columns[i] = random.randint(0, height)
                
                # Draw the character
                if 0 <= columns[i] < height:
                    char = random.choice(chars)
                    screen[columns[i]][i] = char
                    
                    # Add trail
                    for j in range(1, min(5, height - columns[i])):
                        if random.random() < 0.5:
                            screen[columns[i] + j][i] = random.choice(chars)
                
                columns[i] += 1
            
            # Print the screen
            for row in screen:
                print(f"{self.colors['green']}{''.join(row)}{self.colors['reset']}")
            
            time.sleep(0.1)
    
    def create_wave_animation(self, text, width=80, height=24, duration=10):
        """Create a wave animation with text"""
        end_time = time.time() + duration
        
        while time.time() < end_time and self.animation_running:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            # Calculate wave offset based on time
            offset = int((time.time() * 2) % width)
            
            # Create a new screen
            screen = []
            for y in range(height):
                row = []
                for x in range(width):
                    # Calculate wave height at this position
                    wave_height = int(height/2 + height/4 * math.sin((x + offset) * 0.1))
                    
                    if y == wave_height:
                        # Get character from text
                        text_index = x % len(text)
                        row.append(f"{self.colors['cyan']}{text[text_index]}{self.colors['reset']}")
                    else:
                        row.append(' ')
                screen.append(''.join(row))
            
            # Print the screen
            print('\n'.join(screen))
            time.sleep(0.1)
    
    def create_starfield(self, width=80, height=24, duration=10):
        """Create a starfield animation"""
        stars = []
        for _ in range(50):
            stars.append({
                'x': random.randint(0, width-1),
                'y': random.randint(0, height-1),
                'speed': random.uniform(0.1, 0.5),
                'brightness': random.uniform(0.3, 1.0)
            })
        
        end_time = time.time() + duration
        
        while time.time() < end_time and self.animation_running:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            # Create a new screen
            screen = [[' '] * width for _ in range(height)]
            
            # Update and draw stars
            for star in stars:
                # Move star
                star['x'] -= star['speed']
                
                # Reset star if it goes off screen
                if star['x'] < 0:
                    star['x'] = width - 1
                    star['y'] = random.randint(0, height-1)
                
                # Draw star
                if star['brightness'] > 0.7:
                    char = '●'
                elif star['brightness'] > 0.4:
                    char = '•'
                else:
                    char = '·'
                
                screen[star['y']][int(star['x'])] = f"{self.colors['white']}{char}{self.colors['reset']}"
            
            # Print the screen
            for row in screen:
                print(''.join(row))
            
            time.sleep(0.1)
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("ASCII Art Generator - Interactive Mode")
        print("Type 'help' for commands or 'quit' to exit")
        
        while True:
            command = input("> ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                break
            elif command == 'help':
                self.show_help()
            elif command.startswith('image '):
                parts = command.split()
                if len(parts) >= 2:
                    image_path = parts[1]
                    width = int(parts[2]) if len(parts) > 2 else None
                    height = int(parts[3]) if len(parts) > 3 else None
                    charset = parts[4] if len(parts) > 4 else None
                    print(self.image_to_ascii(image_path, width, height, charset))
            elif command.startswith('text '):
                parts = command.split(maxsplit=1)
                if len(parts) >= 2:
                    text = parts[1]
                    print(self.text_to_ascii(text))
            elif command.startswith('banner '):
                parts = command.split(maxsplit=1)
                if len(parts) >= 2:
                    text = parts[1]
                    print(self.text_to_banner(text))
            elif command.startswith('block '):
                parts = command.split(maxsplit=1)
                if len(parts) >= 2:
                    text = parts[1]
                    print(self.text_to_block(text))
            elif command.startswith('3d '):
                parts = command.split(maxsplit=1)
                if len(parts) >= 2:
                    text = parts[1]
                    print(self.text_to_3d(text))
            elif command == 'matrix':
                duration = input("Duration (seconds, default=10): ").strip()
                duration = int(duration) if duration else 10
                self.create_matrix_rain(duration=duration)
            elif command == 'wave':
                text = input("Text to animate: ").strip()
                duration = input("Duration (seconds, default=10): ").strip()
                duration = int(duration) if duration else 10
                self.create_wave_animation(text, duration=duration)
            elif command == 'starfield':
                duration = input("Duration (seconds, default=10): ").strip()
                duration = int(duration) if duration else 10
                self.create_starfield(duration=duration)
            elif command.startswith('charset '):
                parts = command.split()
                if len(parts) >= 2 and parts[1] in self.charsets:
                    self.current_charset = parts[1]
                    print(f"Charset changed to {parts[1]}")
            elif command.startswith('color '):
                parts = command.split()
                if len(parts) >= 2 and parts[1] in self.colors:
                    self.current_color = parts[1]
                    print(f"Color changed to {parts[1]}")
            else:
                print("Unknown command. Type 'help' for available commands.")
    
    def show_help(self):
        """Show help information"""
        help_text = """
Available Commands:
  help                     - Show this help message
  quit/exit                - Exit the program
  
  image <path> [width] [height] [charset] - Convert image to ASCII
  text <text>              - Convert text to ASCII
  banner <text>            - Create banner-style text
  block <text>             - Create block-style text
  3d <text>                - Create 3D-style text
  
  matrix                   - Show Matrix rain animation
  wave                     - Show wave animation
  starfield                - Show starfield animation
  
  charset <name>           - Change charset (standard, simple, blocks, detailed, binary, dots, lines)
  color <name>             - Change color (red, green, yellow, blue, magenta, cyan, white)
"""
        print(help_text)

def main():
    parser = argparse.ArgumentParser(description='ASCII Art Generator')
    parser.add_argument('--image', help='Path to image file or URL')
    parser.add_argument('--text', help='Text to convert to ASCII')
    parser.add_argument('--width', type=int, default=80, help='Width of ASCII art')
    parser.add_argument('--height', type=int, default=24, help='Height of ASCII art')
    parser.add_argument('--charset', default='standard', 
                        choices=['standard', 'simple', 'blocks', 'detailed', 'binary', 'dots', 'lines'],
                        help='Character set to use')
    parser.add_argument('--color', default='white',
                        choices=['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'],
                        help='Color to use')
    parser.add_argument('--style', choices=['banner', 'block', '3d'], 
                        help='Text style')
    parser.add_argument('--animation', choices=['matrix', 'wave', 'starfield'],
                        help='Animation to play')
    parser.add_argument('--duration', type=int, default=10, 
                        help='Duration of animation in seconds')
    parser.add_argument('--interactive', action='store_true',
                        help='Run in interactive mode')
    
    args = parser.parse_args()
    
    generator = ASCIIArtGenerator()
    
    if args.interactive:
        generator.interactive_mode()
    elif args.animation:
        if args.animation == 'matrix':
            generator.create_matrix_rain(width=args.width, height=args.height, duration=args.duration)
        elif args.animation == 'wave':
            text = args.text if args.text else "ASCII WAVE"
            generator.create_wave_animation(text, width=args.width, height=args.height, duration=args.duration)
        elif args.animation == 'starfield':
            generator.create_starfield(width=args.width, height=args.height, duration=args.duration)
    elif args.image:
        print(generator.image_to_ascii(args.image, args.width, args.height, 
                                     generator.charsets[args.charset], args.color))
    elif args.text:
        if args.style == 'banner':
            print(generator.text_to_banner(args.text, args.color))
        elif args.style == 'block':
            print(generator.text_to_block(args.text, args.color))
        elif args.style == '3d':
            print(generator.text_to_3d(args.text, args.color))
        else:
            print(generator.text_to_ascii(args.text, args.style, args.color))
    else:
        generator.interactive_mode()

if __name__ == "__main__":
    main()
