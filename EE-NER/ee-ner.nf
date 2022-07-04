#!/usr/bin/env nextflow
 
params.ontology = "out_repositoriev6.owl"
onto = file(params.ontology)

process detectEntites {

    echo true
    //conda 'requisites.yml'

    output:
    val "questions.csv" into entitiesCh

    script:

    """
    cd ${baseDir}
    python3 detectEntities.py questionsBase.csv
    """

}


process createTemplate {

    echo true
    input:
        val questions from entitiesCh

    output:
        val "questions_ents.csv" into templatesCh


    script:
    """
    cd ${baseDir}
    python3 createTemplates.py ${questions}

    """

}


process createQuestions {

    echo true
    input:
        val questions from templatesCh

    script:

    """
    cd ${baseDir}
    python3 createQuestions.py ${questions}

    """

}