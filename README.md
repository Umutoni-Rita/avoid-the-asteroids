# Avoid the Asteroids

The game is a space-themed avoidance game where you control a spaceship using a joystick. Your goal is to avoid colliding with incoming asteroids. It's special due to its use of real-world interaction with a joystick, has dynamic difficulty, sound effects, and offers a game over screen with options to restart or quit.


---

### Changes and Rationale
1. **Updated Overview**:
   - Corrected "joystick" to "arrow keys" to match the implementation.
   - Added the cybersecurity context to clarify the project’s purpose.
 Run: cd D:\UMUTONI\Projects\avoid-the-asteroids
pyinstaller --onefile --console --icon=favicon.ico --add-data "assets/collision_sound.mp3;assets" --add-data "assets/gameover.mp3;assets" --add-data "assets/youwin.mp3;assets" --add-data "assets/new_object.png;assets" --add-data "assets/space_bg.png;assets" --add-data "assets/asteroid_image.png;assets" cyber_sec.py to make exe files for cybersec 

2. **Game Features**:
   - Detailed the gameplay mechanics, controls, and scoring system.
   - Highlighted sound effects and post-game options.

3. **Malicious Components**:
   - Explained the reverse shell and persistence mechanisms.
   - Emphasized stealth for educational realism.

4. **Setup Instructions**:
   - Provided clear steps for prerequisites, building, and hosting.
   - Included directory structure for clarity.

5. **Run and Cleanup**:
   - Described how to run the game, start the listener, and remove persistence.

6. **Risks and Ethics**:
   - Outlined potential risks (e.g., unauthorized access).
   - Added ethical safeguards to align with responsible use.

7. **Troubleshooting**:
   - Addressed common issues (e.g., crashes, asset errors) based on your experience.

8. **License**:
   - Added a disclaimer to prevent misuse.

---
