package nlp.articles

import chalk.lang.eng.Twokenize
import nak.util.ConfusionMatrix
import scala.xml.Elem

object Lexicon {

    def apply(eval: List[Elem], detailed: Boolean) {
        val evalLabels = (for(file <- eval) yield
            (file \\ "item").map(item => (item \ "@label").text).toList
        ).flatten
        val evalText = (for(file <- eval) yield
            (file \\ "content").map(_.text).toList
        ).flatten
        
        val predictions = (for(text <- evalText) yield getSentiment(text))
        val cm = ConfusionMatrix(evalLabels, predictions, evalText)
        println(cm)
        if(detailed)
            println(cm.detailedOutput)
    }
    
    def getSentiment(text: String): String = {
        val tokens = Twokenize(text)
        val polarity = English.getPolarity(tokens)
        return polarity match {
            case 0 => "positive"
            case 1 => "negative"
            case 2 => "neutral"
        }
    }
}
