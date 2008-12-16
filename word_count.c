int main()
{
  int com_c, c, lst_c, chr_count, line_count, word_count;
  int state = 1;
  int com_state = 0;

  lst_c = -99;
  chr_count = line_count = word_count = 0;
  while ((c = getchar()) != (-1))
  {

    if (c == '*' && lst_c == '/') { com_state = 1; com_c = lst_c;}
    while (com_state == 1)
    {
      lst_c = c;
      c = getchar();
      if (c == '/' && lst_c == '*') { com_state = 0; lst_c = com_c; c = getchar(); }
    }

    if (c == '/' && lst_c == '/') { com_state = 1; com_c = lst_c; }
    while (com_state == 1)
    {
      lst_c = c;
      c = getchar();
      if (c == '\n') { com_state = 0; lst_c = com_c; c = getchar(); }
    }

    chr_count += 1;

    if (c == '\n') { line_count += 1; }

    if (c == '\n' || c == '\t' || c == ' ')
    {
      if (state == 1)
      {
        word_count += 1;
      }
      state = 0;
    }
    else if (state == 0)
    {
      state = 1;
    }
    putchar(c);

    lst_c = c;
  }

  if (lst_c != -99 && lst_c != '\n') { line_count += 1; putchar((int)'\n'); }
  if (lst_c != -99 && lst_c != '\n' && lst_c != '\t' && lst_c != ' ') { word_count += 1; }

  printf("Number of Characters: %d\n", chr_count);
  printf("Number of Words: %d\n", word_count);
  printf("Number of Lines: %d\n", line_count);
}
