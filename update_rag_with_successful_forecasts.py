from error import error
from plot_community_errors import plot_community_errors

def update_rag_with_successful_forecasts(df, rag, live):
    df['error'] = df.apply(error, axis=1)
    success_mask = df.error < df.error.quantile(0.25)
    for _, row in df[success_mask].iterrows():
        rag.add_to_index(row['research'], row['id_of_question'])
    plot_community_errors(df)
    return df