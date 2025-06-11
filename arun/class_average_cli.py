import sqlite3
import pandas as pd
import click

def compute_mean_by_well_and_class(conn, class_column, measurement_column):
    image_df = pd.read_sql("SELECT ImageNumber, Image_Metadata_Well FROM MyExpt_Per_Image", conn)
    
    query = f"""
        SELECT ImageNumber, {class_column}, {measurement_column}
        FROM MyExpt_Per_Object
        """
    object_df = pd.read_sql(query, conn)
    merged_df = object_df.merge(image_df, on="ImageNumber")

    result = (
        merged_df
        .groupby(["Image_Metadata_Well", class_column])
        [measurement_column]
        .mean()
        .reset_index()
    )
    result.columns = ["Well", "Class", f"Mean_{measurement_column}"]
    return result

@click.command()
@click.argument("database", type=click.Path(exists=True))
@click.argument("class_column", type=str)
@click.argument("measurement_column", type=str)
@click.option("--output", "-o", type=click.Path(), default=None, help="Path to save output CSV file")
def main(database, class_column, measurement_column, output):
    """
    Compute the mean of MEASUREMENT_COLUMN grouped by well and class from an SQLite DATABASE.
    """
    conn = sqlite3.connect(database)
    
    try:
        result_df = compute_mean_by_well_and_class(conn, class_column, measurement_column)
        if output:
            result_df.to_csv(output, index=False)
            click.echo(f"Results written to: {output}")
        else:
            click.echo(result_df.to_string(index=False))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
