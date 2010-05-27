intro
==================
bmk is a simple build system geared towards C/C++ projects

todo
===================
* make nice library-finding API
* add support for more compilers
* get something building

help is welcome ;)

howto
=================
.bmk files have a simple, elegant synatx, designed to be easy-to-use.

**Example**
<pre>
(start)
  /* starting task for our project */
  depends: main

(main)
  source: foo.cpp bar.cpp
  libs: z
  requires: zlib
  out: ourproject

  [win32]
  source: foo_win32.cpp

  [posix]
  source: foo_posix.cpp
</pre>

simply run "bmk" or "bmk task_you_want_to_run", it will execute, if found, a file called "build.bmk"