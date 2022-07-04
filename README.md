# Question Entity Detection based on Transformers

In this project there are some experiments performed as a part of an investigation task to learn how to detect entities in natural language biomedical questions. For instance: 

<p align="center">
    Is there any correlation between Diabetes Type II and Age in women?
</p>

In the foresaid example, Diabetes Type II is an phenotype and women is a specie. The main complexity of the problem relys on the high variance of the entities. The entities can be in it's formal name, such as Diabetes Type II, using synonyms such as women (Homo Sapiens) or could just not be present in the question at all! These means that the entities should be infered from the context if possible. For example:

<p align="center">
    Are catarcts a common disease in humans?
</p>

The model should infer that the detected tissue is the eye. There are 3 entites to be detected:

1. Specie
2. Phenotype
3. Tissue

3 Experiments were conducted to try to solve this task. Furthermore, the EE-NER experiment tackles only the creation of the labeled dataset, while the other 2 focus on creating the detector as well. 

The experiments are further discribed on their respectives readmes, but a short description is given:

1. **EE-NER**
2. **EE-Especie**
3. **EE-BERT-T5**
