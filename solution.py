datasets = ['a_example', 'b_lovely_landscapes', 'c_memorable_moments', 'd_pet_pictures', 'e_shiny_selfies']
# datasets = ['a_example']

class Photo:
    def __init__(self, photo_id, orientation, tags):
        self.photo_id = photo_id
        self.orientation = orientation
        self.tags = tags

class Slide:
    def __init__(self, slide_id, photos):
        self.slide_id = slide_id
        self.photos = photos
        self.tags = photos[0].tags if len(photos) == 1 else photos[0].tags.union(photos[1].tags)

class SlideShow:
    def __init__(self):
        self.slides = []
        self._ids = set()

    def add_slide(self, slide):
        self.slides.append(slide)
        for photo in slide.photos:
            self._ids.add(photo.photo_id)

    def count_photos(self):
        return len(self._ids)

    def photo_exists(self, photo_id):
        return photo_id in self._ids

    def save(self, dataset):
        f = open('outputs/' + dataset + '_solution.txt', 'w')
        f.write(str(len(self.slides)) + '\n')
        n = len(self.slides)
        for i in range(n):
            f.write(' '.join([str(x.photo_id) for x in self.slides[i].photos]))
            if i < n-1: f.write('\n')

def interest_factor(tags1, tags2):
    return min(len(tags1.intersection(tags2)), len(tags1 - tags2), len(tags2 - tags1))

for dataset in datasets:
    slide_id = 0
    photos = []
    with open('datasets/' + dataset + '.txt') as f:
        photo_count = int(f.readline())
        for i in range(photo_count):
            line = f.readline().rstrip()
            linedata = line.split(' ')
            photos.append(Photo(i, linedata[0], set(linedata[2:])))

    slideshow = SlideShow()
    slides = []

    last_vertical = []
    for photo in photos:
        if photo.orientation == 'H':
            slides.append(Slide(slide_id, [photo]))
            slide_id += 1
        elif len(last_vertical) == 0: last_vertical.append(photo)
        elif len(last_vertical) == 1:
            last_vertical.append(photo)
            slides.append(Slide(slide_id, last_vertical))
            slide_id += 1
            last_vertical = []

    slides_hash = {}
    for i in range(len(slides)):
        slides_hash[i] = sorted(slides[:i] + slides[i+1:], key=lambda x: interest_factor(slides[i].tags, x.tags), reverse=True)

    slideshow.add_slide(slides[0])
    last_added = slides[0]
    for i in range(1, len(slides)):
        nearest_slides = slides_hash[last_added.slide_id]
        j = 0
        while slideshow.photo_exists(nearest_slides[j].photos[0].photo_id): j += 1
        slideshow.add_slide(nearest_slides[j])
        last_added = nearest_slides[j]

    slideshow.save(dataset)


