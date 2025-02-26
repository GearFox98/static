from stutils import media

var = "It works!"
archie = media("btw.png")

def get():
    return f'''
    <div class="card">
        <h1>{var}</h1>
        <img src={archie} />
    </div>
    '''