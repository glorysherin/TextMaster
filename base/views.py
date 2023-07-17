from spellchecker import SpellChecker
from transformers import pipeline
from django.shortcuts import render
import language_tool_python


# Create your views here.
def home(request):
    spell_checker = SpellChecker()

# Initialize summarizer
    summarizer = pipeline("summarization")
    lang_tool = language_tool_python.LanguageTool('en-US')

    if request.method == 'POST':
        text = request.POST['text']
        button = request.POST['button']

        if button == 'original':
            return render(request,'index.html', {'text':text,'button':button})
        elif button == 'grammar':
            corrected_text = lang_tool.correct(text)
            return render(request,'index.html', {'text':text, 'corrected_text':corrected_text, 'button':button})
        elif button == 'spell':
            misspelled = spell_checker.unknown(text.split())
            corrected_spelling_text = ' '.join(spell_checker.correction(word) if word in misspelled else word for word in text.split())
            return render(request,'index.html', {'text':text, 'corrected_spelling_text':corrected_spelling_text, 'button':button})
        elif button == 'summary':
            summary = summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
            return render(request,'index.html',{'text':text, 'summary':summary, 'button':button})
    
    

    return render(request,'index.html')