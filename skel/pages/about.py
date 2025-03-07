import sys

VERSION = f"{sys.version}"

def cards(repeats):
    cards = ""
    for i in range(repeats):
        cards = cards + f'''
        <div class="col-sm-6 mb-3 mb-sm-0">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Card {i}</h5>
                    <h6 class="card-subtitle mb-2 text-body-secondary">Generated card</h6>
                    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                    <a href="#" class="card-link">Card link</a>
                </div>
            </div>
        </div>
    '''
    
    return cards

def get():
    return f'''
    <div class="container p-5">
        <h2>Static v1.0-3</h2>
        <p>
            A static web site generator inspired by React and written in <strong>Python 🐍</strong><br/>
            Static gives complete flexibility for building the site as it just focus on sew the pieces together. All you require is basic web programing skills and a bit of Python!
        </p>

        <h6>You're running Python {VERSION}</h6>
        <div class="dgrid py-2">
            <a class="btn btn-warning" href="index.html">Back</a>
        </div>

        <h3 class="py-3">Generated card group</h3>
        <div class="row gy-3">
            {cards(8)}
        </div>
    </div>
    '''