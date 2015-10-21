package se.uu.csproject.monadclient.recyclerviews;

import android.support.v7.widget.CardView;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.List;

import se.uu.csproject.monadclient.R;

public class LanguageRecyclerViewAdapter
        extends RecyclerView.Adapter<LanguageRecyclerViewAdapter.LanguageViewHolder> {

    private List<Language> languages;
    private int selectedLanguagePosition=100;

    public class LanguageViewHolder extends RecyclerView.ViewHolder
            implements View.OnClickListener{

        CardView languageCard;
        ImageView languageFlag;
        TextView languageName;

        LanguageViewHolder(View itemView) {
            super(itemView);
            languageCard = (CardView) itemView.findViewById(R.id.card_language);
            languageFlag = (ImageView) itemView.findViewById(R.id.icon_flag);
            languageName = (TextView) itemView.findViewById(R.id.label_language);

            itemView.setOnClickListener(this);
        }

        @Override
        public void onClick(View v) {
            languageCard.setCardBackgroundColor(R.color.accentColor);
            languageName.append(String.valueOf(getAdapterPosition()));
            selectedLanguagePosition = getAdapterPosition();
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
        LanguageViewHolder languageViewHolder = new LanguageViewHolder(view);
        return languageViewHolder;
    }

    @Override
    public void onBindViewHolder(LanguageViewHolder languageViewHolder, int i) {
        languageViewHolder.languageName.setText(languages.get(i).name);
        languageViewHolder.languageFlag.setImageResource(languages.get(i).flagId);
    }

    @Override
    public int getItemCount() {
        return languages.size();
    }
}
