import atexit
from py4j_server import launch_py4j_server
from py4j.java_gateway import java_import

gateway = launch_py4j_server()
java_import(gateway.jvm, "simplenlg.features.*")
java_import(gateway.jvm, "simplenlg.realiser.*")
atexit.register(gateway.close)

class Linearizer ():

    def __init__ (self, **kwds):
        pass

    def linearize (self):
        jvm = gateway.jvm

        phrase = jvm.SPhraseSpec()

        recipe_type = jvm.NPPhraseSpec("recipes")
        recipe_type.addModifier("breakfast")
        recipe_type.addModifier("Mexican")

        prep = jvm.PPPhraseSpec()
        prep.setPreposition("that contain")
        prep.addComplement("cheese")
        prep.addComplement("salsa")
        prep.addComplement("eggs")
        recipe_type.addModifier(prep)

        phrase.setInterrogative(jvm.InterrogativeType.YES_NO)
        phrase.setSubject("you")
        phrase.setVerb("want")
        phrase.addComplement(recipe_type)

        realiser = jvm.Realiser()
        result = realiser.realiseDocument(phrase).strip()
        return result
