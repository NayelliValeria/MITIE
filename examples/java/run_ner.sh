export LD_LIBRARY_PATH=../../mitielib 
export CLASSPATH=../../mitielib/javamitie.jar:. 

javac nerExample.java

java nerExample ../../sample_text.txt  ../../MITIE-models/english/ner_model.dat ../../MITIE-models/english/binary_relations/rel_classifier_people.person.place_of_birth.svm
