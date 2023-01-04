package main

import (
	"context"
	"github.com/gin-gonic/gin"
	logging "github.com/sirupsen/logrus" //github.com/sirupsen/logrus
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
	"net/http"
	"strconv"
)

func main() {
	MongoDB()
	r := gin.Default()
	//r.Delims("{[{", "}]}")  默认是"{{","}}"
	r.LoadHTMLGlob("templates/*")
	r.Static("/img", "../Images")
	r.GET("list/:page_num", listItem)
	r.Run()
}

func listItem(c *gin.Context) {
	pageNum, err := strconv.Atoi(c.Param("page_num"))
	pageSize := 100
	var pageLen int
	skip := pageSize * pageNum
	cursor, err := collection.Find(c, bson.M{}, options.Find().SetLimit(int64(pageSize)).SetSkip(int64(skip)))

	//total := totalCursor
	if err != nil {
		log.Fatal(err)
	}
	total, err := collection.CountDocuments(c, bson.M{})
	if err != nil {
		log.Fatal(err)
	}
	pageLen = int(total) / pageSize
	var episodes []bson.M
	if err = cursor.All(c, &episodes); err != nil {
		log.Fatal(err)
	}
	//pageList := [pageLen]int{}
	pages := make([]int, pageLen)
	for i := 0; i < pageLen; i++ {
		pages[i] = i + 1
	}
	c.HTML(http.StatusOK, "index.tmpl", gin.H{
		"items": episodes,
		"pages": pages,
	})

}

func iphoneAPI(c *gin.Context) {

}

var MongoDBClient *mongo.Client
var collection *mongo.Collection

func MongoDB() {
	// 设置mongoDB客户端连接信息
	clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")
	var err error
	MongoDBClient, err = mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		logging.Error(err)
	}
	err = MongoDBClient.Ping(context.TODO(), nil)
	if err != nil {
		logging.Error(err)
	}
	logging.Info("MongoDB Connect")
	collection = MongoDBClient.Database("zhuanzhuanD").Collection("iphone")
}
