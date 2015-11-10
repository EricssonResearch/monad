package se.uu.csproject.monadclient.recyclerviews;

import android.support.v7.widget.CardView;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.List;

import se.uu.csproject.monadclient.ClientAuthentication;
import se.uu.csproject.monadclient.R;

public class LanguageRecyclerViewAdapter
        extends RecyclerView.Adapter<LanguageRecyclerViewAdapter.LanguageViewHolder> {

    private List<Language> languages;

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
            selectedOverlay = (View) itemView.findViewById(R.id.selected_overlay);
        }
    }

    public LanguageRecyclerViewAdapter(List<Language> languages){
        this.languages = languages;
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
        languageViewHolder.languageCard.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                languageViewHolder.selectedOverlay.setVisibility(View.VISIBLE);
                ClientAuthentication.setLanguage(languages.get(i).index);
                Toast.makeText(languageViewHolder.languageCard.getContext(), "Language changed to " + ClientAuthentication.getLanguage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    @Override
    public int getItemCount() {
        return languages.size();
    }
}
