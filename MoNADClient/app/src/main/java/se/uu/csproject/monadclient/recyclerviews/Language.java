package se.uu.csproject.monadclient.recyclerviews;

//TODO (low priority): add a variable to determine the locale to be used in the app
public class Language{
    String name;
    String index;
    int flagId;

    public Language(String name, String index, int flagId) {
        this.name = name;
        this.index= index;
        this.flagId = flagId;
    }
}
