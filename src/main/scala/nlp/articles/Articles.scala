package nlp.articles

object Articles {
    print("cool cool")
    import com.codahale.jerkson.Json._
    def main(args: Array[String]) {
        val articles = parse[Map[String, Map[String, String]]](readFile(args(0)))
        for((sym, dateArticleMap) <- articles) {
            println(sym)
        }
    }
    
    def readFile(fname:String):String = {
        val source = scala.io.Source.fromFile(fname)
        val lines = source.mkString
        source.close()
        return lines
    }
}
