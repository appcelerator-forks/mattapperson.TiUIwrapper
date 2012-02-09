# TiUIWrapper

The TiUIWrapper plugin auto generates a wrapper plugin for whatever Titanium SDK your using, and auto regenerates only when you need to.
It creates a wrapper for any UI object you use, and only the ones you need to save on space.

To understand why you NEED a wrapper in Titanium, see [this Appcelerator blog post](http://developer.appcelerator.com/blog/2012/02/what-is-a-titanium-proxy-object.html)

And yes it is 100% cross platform :)

So what is better about TiUIWrapper over others that are out there?
TiUIWrapper is auto generated based on the code you write in your app, and the Titanium APIs... so if Appcelerator adds a new UI elements, its automaticly in TiUIWrapper!

Also, it auto creates passthroughs for methods so you can use less code then any other wrapper, and its easier to use.

On top of all that, 2 new methods are added to all UI components, onDestroy(), and release()

onDestroy() is used to take actions when a UI element is being released, think like the close event listener on a window, but for views

release() is used in place of making a proxy = undefined, but also clears things like background images to make sure ALL memory is released in a single command.

## This Plugin

You reference your plugin in the application `tiapp.xml` file such as:

    <plugins>
        <plugin version="0.4">ti.proxy.manager</plugin>
    </plugins>

You then add your plugin directly to your project. Copy your `plugin.py` to the directory
`$PROJECT_DIR/plugins/ti.proxy.manager/0.4/`.


# Sample Application

The `example/` folder contains a very simple `app.js` as a proof-of-concept.  You can copy that file into a new project, then run the project to see how it works.

For now you also need to copy in the blank `TiUIwrapper.js` file too... I will fix that ASAP

# To-DO

See the issues tab...

# License

The code is Copyright 2012 by Matthew Apperson, and made available under the Apache 2.0 license.

# Disclaimers

This is a private project of mine. If you have issues, please file them in the GitHub Issues section of the repository and I will try to get to them in a timely fashion.