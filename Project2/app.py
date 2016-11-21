from flask import Flask, render_template, request
import json
import os
app = Flask(__name__)

@app.route('/')
def questions():
    if request.args:
        if os.path.getsize('data.json') == 0:
            jf = open('data.json', 'w')
            s = []
            json.dump(s, open('data.json', 'w'))
        lst = json.load(open('data.json', 'r'))
        if len(request.args)!=0:
            lst.append(request.args)
        json.dump(lst, open('data.json', 'w'))
        ed = open('education.txt', 'a')
        ed.write(request.args['education'] + '\n')
        ed.close() #записали данные об образовании респондентов
        if request.args['sex']=='male':
            male = open('male.txt', 'a')
            male.write(request.args['tv'] + '\n' + request.args['sv'] + '\n' + request.args['sc'] + '\n')
            male.close()
        elif request.args['sex']=='female':
            female = open('female.txt', 'a')
            female.write(request.args['tv'] + '\n' + request.args['sv'] + '\n' + request.args['sc'] + '\n')
            female.close()
    return render_template('questions.html')

@app.route('/json')
def js():
    lst = json.load(open('data.json', 'r'))
    return render_template('json.html', lst=lst)

@app.route('/stats')
def stats():
    tvOrog, tvorOg, svEkla, sveklA, schAvel, schavEl, tv_total, sv_total, sc_total, total_len = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    women_total, men_total = 0, 0
    edu_mid, edu_mid_prof, edu_high_nf, edu_high, edu_mid_total, edu_mid_prof_total, edu_high_nf_total, edu_high_total, edu_total = 0, 0, 0, 0, 0, 0, 0, 0, 0
    ed_file = open('education.txt', 'r')
    for line in ed_file:
        if line=='mid\n':
            edu_mid += 1
        elif line=='mid_prof\n':
            edu_mid_prof += 1
        elif line=='high_nf\n':
            edu_high_nf += 1
        elif line=='high\n':
            edu_high += 1
    ed_file.close()
    w_file = open('female.txt', 'r')
    for line in w_file:
        women_total += 1
        if line=='tvOrog\n':
            tvOrog += 1
        elif line=='tvorOg\n':
            tvorOg += 1
        elif line=='svEkla\n':
            svEkla += 1
        elif line=='sveklA\n':
            sveklA += 1
        elif line=='schAvel\n':
            schAvel += 1
        elif line=='schavEl\n':
            schavEl += 1
    w_file.close()
    m_file = open('male.txt', 'r')
    for line in m_file:
        men_total += 1
        if line=='tvOrog\n':
            tvOrog += 1
        elif line=='tvorOg\n':
            tvorOg += 1
        elif line=='svEkla\n':
            svEkla += 1
        elif line=='sveklA\n':
            sveklA += 1
        elif line=='schAvel\n':
            schAvel += 1
        elif line=='schavEl\n':
            schavEl += 1
    m_file.close()
    tv_total = int(tvOrog) + int(tvorOg)
    tvOrog = int(tvOrog) * 100 // int(tv_total)
    tvorOg = int(tvorOg) * 100 // int(tv_total)
    sv_total = int(svEkla) + int(sveklA)
    svEkla = int(svEkla) * 100 // int(sv_total)
    sveklA = int(sveklA) * 100 // int(sv_total)
    sc_total = int(schAvel) + int(schavEl)
    schAvel = int(schAvel) * 100 // int(sc_total)
    schavEl = int(schavEl) * 100 // int(sc_total)
    women_total = int(women_total) * 100 // int(int(women_total)+int(men_total))
    men_total = 100 - int(women_total)
    edu_total = int(edu_mid) + int(edu_mid_prof) + int(edu_high_nf) + int(edu_high)
    edu_mid_total = int(edu_mid) * 100 // int(edu_total)
    edu_mid_prof_total = int(edu_mid_prof) * 100 // int(edu_total)
    edu_high_nf_total = int(edu_high_nf) * 100 // int(edu_total)
    edu_high_total = int(edu_high) * 100 // int(edu_total)
    return render_template('statistics.html', tvOrog=tvOrog, tvorOg=tvorOg, svEkla=svEkla, sveklA=sveklA, schAvel=schAvel, schavEl=schavEl, women_total=women_total, men_total=men_total, edu_mid_total=edu_mid_total, edu_mid_prof_total=edu_mid_prof_total, edu_high_nf_total=edu_high_nf_total, edu_high_total=edu_high_total)

@app.route('/search')
def search():
    if request.args:
        gender = request.args['gender']
        word = request.args['word']
        if request.args['gender']=='women':
            fil = open('female.txt', 'r')
            fst_syl, snd_syl, all_var, fst_total, snd_total = 0, 0, 0, 0, 0
            for line in fil:
                if request.args['word']=='tvorog':
                    if line=='tvOrog\n':
                        fst_syl += 1
                        all_var += 1
                    elif line=='tvorOg\n':
                        snd_syl += 1
                        all_var += 1
                elif request.args['word']=='svekla':
                    if line=='svEkla\n':
                        fst_syl += 1
                        all_var += 1
                    elif line=='sveklA\n':
                        snd_syl += 1
                        all_var += 1
                elif request.args['word']=='schavel':
                    if line=='schAvel\n':
                        fst_syl += 1
                        all_var += 1
                    elif line=='schavEl\n':
                        snd_syl += 1
                        all_var += 1
            fst_total = int(fst_syl)*100//int(all_var)
            snd_total = int(snd_syl)*100//int(all_var)
            fil.close()
        elif request.args['gender']=='men':
            fil = open('male.txt', 'r')
            fst_syl, snd_syl, all_var, fst_total, snd_total = 0, 0, 0, 0, 0
            for line in fil:
                if request.args['word']=='tvorog':
                    if line=='tvOrog\n':
                        fst_syl += 1
                        all_var += 1
                    elif line=='tvorOg\n':
                        snd_syl += 1
                        all_var += 1
                elif request.args['word']=='svekla':
                    if line=='svEkla\n':
                        fst_syl += 1
                        all_var += 1
                    elif line=='sveklA\n':
                        snd_syl += 1
                        all_var += 1
                elif request.args['word']=='schavel':
                    if line=='schAvel\n':
                        fst_syl += 1
                        all_var += 1
                    elif line=='schavEl\n':
                        snd_syl += 1
                        all_var += 1
            fst_total = int(fst_syl)*100//int(all_var)
            snd_total = int(snd_syl)*100//int(all_var)
            fil.close()
        return render_template('results.html', gender=gender, word=word, fst_total=fst_total, snd_total=snd_total)
    return render_template('search.html')

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
