package se.uu.csproject.monadclient.recyclerviews;

import android.content.Context;
import android.content.res.Configuration;
import android.support.v7.widget.CardView;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.List;
import java.util.Locale;

import se.uu.csproject.monadclient.ClientAuthentication;
import se.uu.csproject.monadclient.MainActivity;
import se.uu.csproject.monadclient.R;
import se.uu.csproject.monadclient.SettingsActivity;

public class LanguageRecyclerViewAdapter
        extends RecyclerView.Adapter<LanguageRecyclerViewAdapter.LanguageViewHolder> {

    private List<Language> languages;
    private View selectedCardView;
    //private Context parentContext;

    public class LanguageViewHolder extends RecyclerView.ViewHolder {

        CardView languageCard;
        ImageView languageFlag;
        TextView languageName;
        View selectedOverlay;

        LanguageViewHolder(View itemView) {
            super(itemView);
            languageCard = (CardView) itemView.findViewById(R.id.card_language);
            languageFlag = (ImageView) itemView.findViewById(R.id.icon_flag);
            languageName = (TextView) itemView.findViewById(R.id.label_language);
            selectedOverlay = itemView.findViewById(R.id.selected_overlay);
        }
    }

    public LanguageRecyclerViewAdapter(Context context, List<Language> languages){
        this.languages = languages;
        //this.parentContext = context;
    }

    @Override
    public void onAttachedToRecyclerView(RecyclerView recyclerView) {
        super.onAttachedToRecyclerView(recyclerView);
    }

    @Override
    public LanguageViewHolder onCreateViewHolder(ViewGroup viewGroup, int i) {
        View view = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.list_item_language,
                viewGroup, false);
        return new LanguageViewHolder(view);
    }

    @Override
    public void onBindViewHolder(final LanguageViewHolder languageViewHolder, final int i) {
        languageViewHolder.languageName.setText(languages.get(i).name);
        languageViewHolder.languageFlag.setImageResource(languages.get(i).flagId);
        if(ClientAuthentication.getLanguage().equals(languages.get(i).index)){
            languageViewHolder.selectedOverlay.setVisibility(View.VISIBLE);
            selectedCardView = languageViewHolder.selectedOverlay;
        }
        languageViewHolder.languageCard.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                selectedCardView.setVisibility(View.INVISIBLE);
                languageViewHolder.selectedOverlay.setVisibility(View.VISIBLE);
                selectedCardView = languageViewHolder.selectedOverlay;
                ClientAuthentication.setLanguage(languages.get(i).index);
                ClientAuthentication.setIfSettingsChanged(true);
                Toast.makeText(languageViewHolder.languageCard.getContext(), languageViewHolder.itemView.getResources().getString(R.string.java_languagerva_languagechanged) + " " + ClientAuthentication.getLanguage(), Toast.LENGTH_SHORT).show();

                Locale locale = new Locale(languages.get(i).index);
                Locale.setDefault(locale);
                Configuration config = new Configuration();
                config.locale = locale;
                languageViewHolder.itemView.getContext().getResources().updateConfiguration(config,
                        languageViewHolder.itemView.getContext().getResources().getDisplayMetrics());
                //parentContext.startActivity(((SettingsActivity) parentContext).getIntent());
                //((SettingsActivity) parentContext).finish();
            }
        });
    }

    @Override
    public int getItemCount() {
        return languages.size();
    }
}
