import json
from collections import OrderedDict

from PIL import Image
from PIL import ImageDraw

import R
from layout.Resource import Resource

from pydoc import locate


class Form(Resource):
    def __init__(self, name):
        Resource.__init__(self, name)
        R.init()  # Initialize resources
        # https://pillow.readthedocs.io/en/3.1.x/handbook/concepts.html#concept-modes
        # L (8-bit pixels, black and white)
        if R.config.ORIENTATION == R.LANDSCAPE:
            self.mMask = Image.new('1', (R.config.WIDTH, R.config.HEIGHT), 255)
        else:
            self.mMask = Image.new('1', (R.config.HEIGHT, R.config.WIDTH), 255)

        self.mDraw = None
        self.mLayout = None
        self.mChildren = OrderedDict()
        self.loadlayout(self.layout)

    @property
    def layout(self):
        if self.mLayout is None:
            if R.config.ORIENTATION == R.LANDSCAPE:
                resource = "res/layout/{0}.json".format(self.name)
            else:
                resource = "res/layout-portrait/{0}.json".format(self.name)
            with open(resource) as f:
                self.mLayout = json.load(f)
        return self.mLayout[self.name]

    @layout.setter
    def layout(self, value):
        self.mLayout = value

    @property
    def children(self):
        return self.mChildren

    @property
    def mask(self):
        return self.mMask

    @mask.setter
    def mask(self, value):
        self.mMask = value

    @property
    def draw(self):
        if self.mDraw is None:
            self.mDraw = ImageDraw.Draw(self.mask)
        return self.mDraw

    def add(self, resource, x=None, y=None):
        resource.parent = self
        if x is not None:
            resource.x = x
        if y is not None:
            resource.y = y
        self.children.update({resource.name: resource})

    def loadlayout(self, layout):
        # locate classes from layout and create their instances dynamically
        for resource in layout:
            classname = layout[resource]["class"]
            obj = locate(classname)(resource)
            if "loadlayout" in dir(obj):
                obj.loadlayout(layout[resource])
                self.add(obj)

    def createview(self):
        for name in self.children:
            if name in self.layout:
                resource = self.children[name]
                resource.createview()

    def save(self, output):
        if R.config.ORIENTATION == R.PORTRAIT:
            out = self.mask.rotate(-90, expand=True)
        else:
            out = self.mask.rotate(0, expand=True)
        out.save(output, "bmp")
