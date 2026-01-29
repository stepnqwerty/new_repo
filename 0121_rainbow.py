import time, os, math, colorsys

def rainbow_spiral():
    width, height = 80, 24
    center_x, center_y = width // 2, height // 2
    duration = 30  # seconds
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            t = time.time() - start_time
            screen = [[' ' for _ in range(width)] for _ in range(height)]
            
            for angle in range(0, 360, 3):
                for r in range(1, min(width, height) // 2):
                    # Convert polar to cartesian coordinates
                    x = int(center_x + r * math.cos(math.radians(angle + t * 50)))
                    y = int(center_y + r * math.sin(math.radians(angle + t * 50)))
                    
                    if 0 <= x < width and 0 <= y < height:
                        # Calculate color based on angle and time
                        hue = (angle + t * 30) % 360 / 360
                        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                        color_code = f"\033[38;2;{int(rgb[0]*255)};{int(rgb[1]*255)};{int(rgb[2]*255)}m"
                        screen[y][x] = f"{color_code}●\033[0m"
            
            print('\n'.join(''.join(row) for row in screen))
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nRainbow spiral ended.")

if __name__ == "__main__":
    rainbow_spiral()
