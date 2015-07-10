# Installing grpc + Python on Mac OSX

1. make a Python virtual environment

        mkvirtualenv --python=python2.7 grpc

2. make a parent directory

        cd src
        mkdir google-rpc
        cd google-rpc

3. download, build, and install protobuf core

        git clone https://github.com/google/protobuf.git

        # install autotools on OSX
        # this makes it "build like UNIX"
        sudo port install autoconf automake libtool

        cd protobuf
        # pre-generate some stuff
        ./autogen.sh
    
        # You may need to point at correct C++ compiler, i.e.
        # the XCode one and not some bullsh_t installed by macports
        export CXX=/usr/bin/g++
    
        # standard build procedure
        ./configure
        make
        make check
        sudo make install # installs to /usr/local/lib ; /usr/local/include/google

4. Install protobuf python

        # make sure you're in that virtualenv
        workon grpc
    
        cd python
        python setup.py install

5. download, build, install grpc core

        git clone https://github.com/grpc/grpc.git
    
        cd grpc
        make shared_c static_c
    
        # this is extracted from 'tools/run_tests/build_python.sh'
        # so we use our virtualenv instead of their temporary one
        pip install -r src/python/requirements.txt
        root=`pwd`
        CFLAGS="-I$root/include -std=c89 -Werror" LDFLAGS=-L$root/libs/$CONFIG pip install src/python/src
        pip install src/python/interop

6. Test with code in grpc-common

        cd .. # back up to ~/src/google-rpc, our parent directory
        git clone https://github.com/grpc/grpc-common.git
    
        cd grpc-common/python/helloworld
    
        ./run_codegen
        # no output = OK then; you should have a file 'helloworld_pb2.py'
    
        # Run server; ignore their dumb little run_server.sh
        python greeter_server.py &
    
        # Run client; ditto with run_client.sh
        python greeter_client.py
        # should see: Greeter client received: Hello, you!
        # then I get a pause and a cryptic message: D0708 22:55:58.086970000 140735107101440 iomgr.c:119] Waiting for 1 iomgr objects to be destroyed and executing final callbacks
        # then it exits
        # pause goes away on subsequent runs
    



