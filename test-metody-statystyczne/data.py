import dash_core_components as dcc
import dash_html_components as html

questions = [
    "1. Analiza regresji służy głównie do badania wpływu zmiennych niezależnych na zmienną zależną",
    "2. Zwiększając liczbę badanych osób zwiększamy również moc testu",
    "3. Jeżeli zależy nam na zmniejszeniu przedziału ufności bez strat w zakładanym poziomie ufności, to wystarczy ograniczyć liczbę osób badanych.",
    "4. Moc testu nie wiąże się z błędem II rodzaju",
    "5. Ponieważ uzyskałem wyniki p=0,5 oraz β=0,20 to mogę stwierdzić, że szukane różnice międzygrupowe nie istnieją.",
    "6. Rotacja Varimax zakłada brak korelacji między czynnikami, natomiast rotacja Oblimin na nie pozwala.",
    "7. Korelacja między neurotycznością a lękiem jest bardzo wysoka, dlatego aby ją zbadać potrzeba znacznie większej ilości osób "
            "niż do zweryfikowania korelacji niższej między potrzebą domknięcia poznawczego, a pokorą intelektualną.",
    "8. Jeżeli chcemy mieć większy poziom ufności w szacowaniu średniej danego parametru w populacji, to należy uargumentować "
            "hipotezę jednostronną, dobadać większą ilość osób lub pozwolić na rozszerzenie przedziału ufności.",
    "9. Test Friedmana używamy gdy w modelu badania posiadamy jedna grupę, jedną zmienną zależną mierzoną na skali rangowej oraz wiele pomiarów tej zmiennej",
    "10. Test U Manna-Whitneya używamy gdy posiadamy dwie grupy badanych, zmienną zależną mierzoną na skali rangowej oraz jeden pomair tej zmiennej",
    "11. Model MANCOVA zakłada większą ilość zmiennych niezależnych niż model 1-ANOVA",
    "12. Osoby badane podzielono wg płci. Dlatego też płeć można nazwać zmienną manipulacyjną",
    "13. Osoby badane są w trzech różnych grupach i sprawdza się różnice w zdolności skupiania uwagi. Zmierzono ich IQ jako "
            "dodatkową charakterystykę, dlatego można ją nazwać zmienną kowariancyjną",
    "14. Ilośc badanych osób nie wiąże się błędem II rodzaju",
    "15. II zasada randomizacji zakłada losowy przydział osób badanych do grup wyodrębnionych na podsatwie zmiennych niezależnych"
]

answers = [
    'Analiza regresji używana jest głównie do badania związku miedzy predyktorami a zmienną objasnianą(zależną)',
    'Im wiecej osób badamy, tym bardziej pomniejszamy błąd II rodzaju, więc moc testu wzrasta',
    'Zmniejszenie liczby osób spowoduje odwrotny efekt - przedział ufności rozszerzy się',
    'Ze wzoru wynika coś całkiem innego: moc_testu = 1 - β',
    'Poziom β jest zbyt wysoki (przekracza 0,1). Dlatego lepiej stwierdzić, że "różnic nie zaobserwowano"',
    'Varimax -> brak korelacji, Oblimin -> korelacje',
    'Im wieksza korelacja (większy efekt) tym potrzeba mniejszej próby aby ją zaobserwować',
    'Wszsytkie te czynności pozwalają na zwiększenie przedziału ufności',
    'Co tu duzo gadać, zdanie jest prawdziwe... (zob. wybór testów różnic)',
    'Co tu duzo gadać, zdanie jest prawdziwe... (zob. wybór testów różnic)',
    'Oba modele są jednoczynnikowe (zakałdają 1ną zmienną niezależną). W takim wypadku nie trzeba zapisywać 1ki przed modelem... ale też nie jest to błędem',
    'Płeć pozwala na kalsyfikację osób, dlatego jest zmienną niezależną-klasyfikacyjną',
    'Zmienna kowariancyjna to dodatkowa zmienna charakteryzujaca osoby badane. Mierzona jest na skali ilościowej oraz wiąże się ze zmienną zależną',
    'Im więcej osób zbadamy, tym mniejszy staje się błąd II rodzaju (beta). Oznacza, to że badanie jest bardziej wrażliwe na poszukiwany efekt.',
    'Co tu duzo gadać, zdanie jest prawdziwe...'
]


# print(questions)
# print(answers)
# print(len(answers))

from style import style_question

def MakeQuestions():
    pages = []
    for i in range(1, len(questions) +1):
        page = html.Div(id=f'quest-{i}-container',
                        children=[
                            html.Div(id=f'quest-{i}', children=questions[i-1], style=style_question),
                            dcc.RadioItems(id=f'radio-quest-{i}',
                                           options=[
                                               {'label':'Prawda', 'value':'true'},
                                               {'label':'Fałsz', 'value':'false'}
                                           ],
                                           labelStyle={'display':'block'},
                                           style=style_question),
                            html.Div(id=f'answer-{i}'),
                            html.Br(),
                            html.Div(id=f'next-quest-{i}')
                        ])
        pages.append(page)

    return pages

questionPages = MakeQuestions()
