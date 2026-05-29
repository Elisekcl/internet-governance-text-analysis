# Scrape an IETF working group mailing list archive.
#
# The IETF organises its technical and policy discussions into working
# groups, each with its own mailing list archive. This script scrapes
# one working group at a time: it collects every message in the chosen
# group's archive, parses sender namesand email domains for analysis

library(rvest)
library(stringr)
library(reshape2)
library(robotstxt)


url<-"https://mailarchive.ietf.org/arch/browse/int-area/"
source <- read_html(url)

# Verify the site's robots.txt allows scraping before proceeding.
if (!all(paths_allowed(paths = archive_index_url))) {
  stop("Scraping not permitted by robots.txt for: ", archive_index_url)
}

page<-"/arch/browse/int-area/?page="

stem<-"https://mailarchive.ietf.org/"
df_total = data.frame()



for(var in 1:218)  # Number of pages of archive to scrape.
  
{
  var<as.character(var)   
  file_link<-paste0(page, var)
  file_link1<-paste0(stem, file_link)
  source <- read_html(file_link1)
  urls_docs <- source %>% 
    html_nodes("a") %>%
    html_attr("href") 
  urls_docs_clean<-str_subset(urls_docs, "/arch/msg/int-area")
  urls_docs_clean1<-paste0(stem, urls_docs_clean)
  df <- data.frame(urls_docs_clean1)
  df_total <- rbind(df_total,df)
}

links<-df_total$urls_docs_clean1

url_emails <- function(links) {
  source <- read_html(links)
  body <- source %>%  html_nodes("div.msg-payload")
  body_c <- as.character(body)
  sender<-source %>% html_nodes(xpath = '//*[@id="msg-from"]') 
  sender_c <- as.character(sender)
  date<-source %>% html_nodes(xpath = '//*[@id="msg-date"]') 
  date_c <- as.character(date)
  mat<-list(body=body_c, sender=sender_c, date=date_c)
}

results_intarea<-sapply(links, url_emails)
results_new_intarea<-as.data.frame(t(results_intarea))

save(results_new_intarea, file = "results_new_intarea.Rdata")

results_new1_intarea<-colsplit(results_new_intarea$sender, "&", names = c("sender", "email"))

results_new1_intarea$sender_cl<-gsub('.*">', '', results_new1_intarea$sender)
results_new1_intarea$sender_cl1<-gsub('"', '', results_new1_intarea$sender_cl)
results_new1_intarea$email_cl<-gsub('lt;', '', results_new1_intarea$email)

results_new2_intarea<-colsplit(results_new1_intarea$email, "@", names = c("rest", "domain"))

results_new2_intarea$domain_cl<-sub("\\..*", "", results_new2_intarea$domain)

results_new1_intarea$email_cl1<-gsub('\\&.*', '', results_new1_intarea$email_cl)

results_f_intarea <- cbind(results_new_intarea, results_new1_intarea, results_new2_intarea)


cleanFun <- function(htmlString) {
  return(gsub("<.*?>", "", htmlString))
}

results_f_intarea$body_cl<-cleanFun(results_f_intarea$body)

results_final_intarea <- results_f_intarea[c(-1,-2,-3,-4,-5,-6 )]

results_final_intarea$sender_cl2 <- sub("(\\w+),\\s(\\w+)","\\2 \\1", results_final_intarea$sender_cl1)

results_final_intarea<-unique(results_final_intarea)

write.csv(results_final_intarea,'email_data_intarea.csv')
View(results_final_intarea)

table(results_final_intarea$sender_cl2)
my_table_intarea <-table(results_final_intarea$sender_cl2)
write.table (my_table_intarea, file = "intarea_table_frequency.csv", sep = ",")
