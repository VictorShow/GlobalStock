from flask import Flask
from flask import render_template, request, jsonify
import  re
app = Flask(__name__)
from calculator.ai_calculatro import Calculator
from cabbage.cabbage import Cabbage
from blood.blood import Blood

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move/<path>')
def move(path):
    return render_template(f'{path}.html')

@app.route('/calculator')
def ui_calculator():
    stmt = request.args.get('stmt', 'NONE')
    if(stmt == 'NONE'):
        print('넘어온 값이 없음...')
    else:
        print(f'넘어온 식: {stmt}')
        patt = '[0-9]+'     # 숫자만 입력
        op = re.sub(patt, '', stmt) #연산자만 남음.
        nums = stmt.split(op)
        result = 0
        n1 = int(nums[0])
        n2 = int(nums[1])
        if op == '+': result = n1 + n2
        elif op == '-': result = n1 - n2
        elif op == '*': result = n1 * n2
        elif op == '/': result = n1 / n2
    return jsonify(result = result)

@app.route('/ai_calculator', methods=['POST'])
def ai_calculator():
    num1 = request.form['num1']
    num2 = request.form['num2']
    opcode = request.form['opcode']
    result = Calculator.service(num1, num2, opcode)
    print(f'인공지능 결과값 : {result}')
    render_params = {}
    render_params['result'] = int(result)
    return render_template('ai_calculator.html', **render_params)

@app.route('/cabbage', methods=['POST'])
def cabbage():
    # avg_temp, min_temp, max_temp, rain_fall
    avg_temp = request.form['avg_temp']
    min_temp = request.form['min_temp']
    max_temp = request.form['max_temp']
    rain_fall = request.form['rain_fall']
    print(f'{avg_temp}')
    print(f'{min_temp}')
    print(f'{max_temp}')
    print(f'{rain_fall}')
    cabbage = Cabbage()
    # cabbage.model()
    cabbage.initialize(avg_temp, min_temp, max_temp, rain_fall)
    result = cabbage.service()

    print(f'인공지능 결과값 : {result}')
    render_params = {}
    render_params['result'] = result
    return render_template('cabbage.html', **render_params)


@app.route('/moveblood')
def moveblood():
    return render_template('blood.html')

@app.route('/blood', methods=['POST'])
def blood():
    weight = request.form['weight']
    age = request.form['age']
    blood = Blood()
    blood.initialize(weight, age)
    result = blood.service()

    print(f'인공지능 결과값 : {result}')

    render_params = {}
    render_params['result'] = result
    return render_template('blood.html', **render_params)

if __name__ == '__main__':
    app.run()