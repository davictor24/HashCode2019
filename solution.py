datasets = ['a_example', 'b_lovely_landscapes', 'c_memorable_moments', 'd_pet_pictures', 'e_shiny_selfies']

class Photo:
    def __init__(self, photo_id, orientation, tags):
        self.photo_id = photo_id
        self.orientation = orientation
        self.tags = tags

class SlideShow:
    def __init__(self):
        self.slides = []
        self._ids = []

    def add_slide(self, photos):
        self.slides.append(photos)
        self._ids += [x.photo_id for x in photos]

    def photo_exists(self, photo_id):
        return photo_id in self._ids

    def save(self, dataset):
        f = open('outputs/' + dataset + '_solution.txt', 'w')
        f.write(str(len(self.slides)) + '\n')
        n = len(self.slides)
        for i in range(n):
            f.write(' '.join([str(x.photo_id) for x in self.slides[i]]))
            if i < n-1: f.write('\n')

def interest_factor(tags1, tags2):
    return min(len(tags1.intersection(tags2)), len(tags1 - tags2), len(tags2 - tags1))

for dataset in datasets:
    photos = []
    with open('datasets/' + dataset + '.txt') as f:
        photo_count = int(f.readline())
        for i in range(photo_count):
            line = f.readline().rstrip()
            linedata = line.split(' ')
            photos.append(Photo(i, linedata[0], set(linedata[2:])))

    slideshow = SlideShow()

    for photo in photos:
        slideshow.add_slide([photo])

    slideshow.save(dataset)


