#!/usr/bin/env nextflow
 
params.ontology = "$baseDir/Ontologias/out_repositoriev6.owl"
params.ontoScript = "speciesFromOntology.py"
params.processSpecieScript = "processSpecie.py"
params.questionsScript = "QuestionGeneration.py"
params.mergeDFs = "mergeDFs.py"
params.createModel = "createModel.py"
params.speciesDir = "species"

onto = file(params.ontology)
ontoScript = "$baseDir" + "/" + params.ontoScript
processSpecieScript = "$baseDir" + "/" + params.processSpecieScript
questionsScript = "$baseDir" + "/" + params.questionsScript
mergeScript = "$baseDir" + "/" + params.mergeDFs
modelScript = "$baseDir" + "/" + params.createModel
speciesDir = "$baseDir" + "/" + params.speciesDir

pipes_dir = "$baseDir" + "/question_generation"

questionsDFCount = 0

Channel
    .fromPath("$speciesDir" + "/*").buffer(size:5, remainder:true)
    .set { species_ch }

process getSpecies {

    output:
    stdout into ontoEnd

    script:

    """
    
    echo "Hola no hago nada" 

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

abstractDFs = file('species/*.csv')

if (abstractDFs.size() == 0)
{
process readSpecies {

    conda 'pandas requests'

    input:
    path specie from species_ch
    val x from requisites

    output:
    path specie into questions_ch

    script:
    """
    cd ${baseDir}
    python3 $processSpecieScript ${speciesDir} ${specie} 

    """
    
    

}
}
else
{
    log.info "Species' Abstracts already loaded."
    Channel
    .fromPath("$speciesDir" + "/*.csv")
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
    python3 ${params.questionsScript} ${speciesDir} ${speciesDS} 
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

if (mergeQuestionsDF.size() == 0)
{
process mergeQuestionsDf {

    conda 'pandas gensim'

    input:
    val x from mergeQuestions_ch
    val y from conditional_ch

    output:
    val x into createModel_ch

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
    createModel_ch = Channel.create()
    createModel_ch.bind(1)
    createModel_ch.bind(1)
    createModel_ch.bind(1)
}

conditionalModel_ch = Channel.from( 1..3 )

process createModel {

    echo true
    
    //conda 'modelEnv.yml'

    input:
    val x from createModel_ch
    val y from conditionalModel_ch

    script:
        if (y == 3)
    {
       """
        pip3 install torch torchvision torchaudio
        cp $modelScript ${pipes_dir}
        cd ${pipes_dir}
        python3 ${modelScript}
        """
    }
    else 
    {
        log.info "Valor de y Model: $y"
        """
        cp $mergeScript ${pipes_dir}
        """
    }

}

