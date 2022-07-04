#!/usr/bin/env nextflow
 
params.ontology = "out_repositoriev6.owl"
params.ontoScript = "entitiesFromOntology.py"
params.processSpecieScript = "processSpecie.py"
params.questionsScript = "QuestionGeneration.py"
params.mergeDFs = "mergeDFs.py"
params.experimentScript = "experimentE1.py"
params.entity = "entity"
params.kw = ""
params.model = "t5"
params.finetune = "no"


onto = file(params.ontology)
ontoScript = "$baseDir" + "/" + params.ontoScript
processSpecieScript = "$baseDir" + "/" + params.processSpecieScript
questionsScript = "$baseDir" + "/" + params.questionsScript
mergeScript = "$baseDir" + "/" + params.mergeDFs
experimentScript = "$baseDir" + "/" + params.experimentScript
entitiesDir = "$baseDir" + "/" + params.entity
pipes_dir = "$baseDir" + "/question_generation"

questionsDFCount = 0

Channel
    .fromPath("$entitiesDir" + "/*").buffer(size: (int) ((new File("$entitiesDir" + "/").listFiles().size())), remainder:true)
    .set { species_ch }

process getEntities {

    output:
    stdout into ontoEnd

    script:

    """
    pip install owlready2
    cd ${baseDir}
    python3 $ontoScript ${params.ontology} ${entitiesDir} ${params.kw}  

    """

}

question_generationDir = file('question_generation/')

if(!question_generationDir.exists())
{
process loadRequisites {

    output:
    val "done" into requisites

    script:
    """
    cd ${baseDir}
    git clone https://github.com/patil-suraj/question_generation.git

    """
    
    

}
}
else
{
    log.info "Question_Generation Directory already loaded."
    requisites = Channel.create()
    requisites.bind("done")
    requisites.bind("done")
    requisites.bind("done")
}

abstractDFs = file(entitiesDir + '/*.csv')

if (abstractDFs.size() == 0)
{
process readSpecies {

    echo true
    conda 'pandas requests'

    input:
    path specie from species_ch

    output:
    path specie into questions_ch

    script:
    """
    cd ${baseDir}
    python3 $processSpecieScript ${entitiesDir} ${specie} 

    """
    
    

}
}
else
{
    log.info "Entities' Abstracts already loaded."
    Channel
    .fromPath("$entitiesDir" + "/*.csv")
    .set { questions_ch }

}

questionsDFs = file('question_generation/questions*.csv')

if (questionsDFs.size() == 0)
{
process createQuestions {

    conda 'questionsEnv.yml'
    echo true

    input:
    val x from requisites
    path speciesDS from questions_ch

    output:
    val 1 into mergeQuestions_ch

    script:
    """
    cp $questionsScript ${pipes_dir}
    cd ${pipes_dir}
    python3 ${params.questionsScript} ${entitiesDir} ${speciesDS} 
    """

}
}
else
{
    log.info "Questions' Datasets already loaded."
    mergeQuestions_ch = Channel.create()
    mergeQuestions_ch.bind(1)
    mergeQuestions_ch.bind(1)
    mergeQuestions_ch.bind(1)

}


conditional_ch = Channel.from( 1..3 )

mergeQuestionsDF = file('question_generation/Question*.csv')

if (mergeQuestionsDF.size() == 0 )
{
process mergeQuestionsDf {

    conda 'pandas gensim'

    input:
    val x from mergeQuestions_ch
    val y from conditional_ch

    output:
    val "done" into experiment_ch

    script:
    if (y == 3)
    {
        """
        cp $mergeScript ${pipes_dir}
        cd ${pipes_dir}
        python3 ${mergeScript}
        """
    }
    else 
    {
        log.info "Valor de y Merge: $y"
        """
        cp $mergeScript ${pipes_dir}
        """
    }

}
}
else
{
    log.info "Questions' Datasets already merged."
    experiment_ch = Channel.create()
    experiment_ch.bind("done")
}

process experimentProcess {

    echo true
    conda 'experimentEnv.yml'

    input:
    val x from experiment_ch

    script:

        """
        pip install owlready2 pandas
        cp $onto ${pipes_dir}
        cp $experimentScript ${pipes_dir}
        cd ${pipes_dir}
        python3 ${experimentScript} ${params.model} ${params.finetune}  
        """

}