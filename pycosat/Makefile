pycosat.so: libpicosat.a pycosat.c
	python3 setup.py build_ext --inplace

picosat.o: picosat.c picosat.h
	$(CC) $(CFLAGS) -fPIC -c $<

libpicosat.a: picosat.o
	ar rc $@ picosat.o 


test: pycosat.so
	python3 test_pycosat.py


clean:
	rm -rf build dist *.egg-info
	rm -f *.pyc *.so *.o *.a
