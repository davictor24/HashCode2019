datasets = ['a_example', 'b_lovely_landscapes', 'c_memorable_moments', 'd_pet_pictures', 'e_shiny_selfies']
# datasets = ['c_memorable_moments']

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

    slides_copy = slides[:]
    last_added = slides_copy[0]
    slideshow.add_slide(last_added)
    slides_copy = slides_copy[1:]
    for i in range(1, len(slides)):
        interest_factors = []
        for slide in slides_copy:
            interest_factors.append(interest_factor(last_added.tags, slide.tags))
        max_if = max([x for x in interest_factors])
        for k in range(len(slides_copy)):
            slide = slides_copy[k]
            if interest_factor(last_added.tags, slide.tags) == max_if:
                last_added = slide
                slideshow.add_slide(slide)
                slides_copy = slides_copy[:k] + slides_copy[k+1:]
                break

    slideshow.save(dataset)


