from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Global variables to track square position
square_pos = {
    'x': 50,  # Initial x position
    'y': 50   # Initial y position
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move_square():
    global square_pos
    direction = request.json.get('direction')
    
    # Movement speed in pixels
    speed = 10
    
    # Update position based on direction
    if direction == 'up' and square_pos['y'] > 0:
        square_pos['y'] -= speed
    elif direction == 'down' and square_pos['y'] < 350:  # 400 - 50 (square size)
        square_pos['y'] += speed
    elif direction == 'left' and square_pos['x'] > 0:
        square_pos['x'] -= speed
    elif direction == 'right' and square_pos['x'] < 350:
        square_pos['x'] += speed
    
    return jsonify(square_pos)

# Create templates/index.html with this content:
"""
<!DOCTYPE html>
<html>
<head>
    <title>Move the Square</title>
    <style>
        #game-container {
            width: 400px;
            height: 400px;
            border: 2px solid black;
            position: relative;
            margin: 20px auto;
        }
        #square {
            width: 50px;
            height: 50px;
            background-color: green;
            position: absolute;
            transition: all 0.1s ease;
        }
        #instructions {
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div id="instructions">
        <h2>Move the Square</h2>
        <p>Use arrow keys to move the green square</p>
    </div>
    <div id="game-container">
        <div id="square"></div>
    </div>

    <script>
        const square = document.getElementById('square');
        
        // Set initial position
        square.style.left = '50px';
        square.style.top = '50px';
        
        // Handle keyboard events
        document.addEventListener('keydown', async (event) => {
            let direction = null;
            
            switch(event.key) {
                case 'ArrowUp':
                    direction = 'up';
                    break;
                case 'ArrowDown':
                    direction = 'down';
                    break;
                case 'ArrowLeft':
                    direction = 'left';
                    break;
                case 'ArrowRight':
                    direction = 'right';
                    break;
            }
            
            if (direction) {
                const response = await fetch('/move', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ direction })
                });
                
                const newPos = await response.json();
                square.style.left = newPos.x + 'px';
                square.style.top = newPos.y + 'px';
            }
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
