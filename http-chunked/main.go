package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"time"
)

func main() {
	server := &APIServer{
		engine: gin.Default(),
	}
	server.registryApi()
	server.engine.Run(":38080")
}

type APIServer struct {
	engine *gin.Engine
}

func (s *APIServer) registryApi() {
	registryStream(s.engine)
}

func registryStream(engine *gin.Engine) {
	engine.GET("/stream", func(ctx *gin.Context) {
		w := ctx.Writer
		header := w.Header()
		//在响应头添加分块传输的头字段Transfer-Encoding: chunked
		header.Set("Transfer-Encoding", "chunked")
		header.Set("Content-Type", "text/html")
		w.WriteHeader(http.StatusOK)

		//Flush()方法，好比服务端在往一个文件中写了数据，浏览器会看见此文件的内容在不断地增加。
		w.Write([]byte(`
            <html>
                    <body>
        `))
		w.(http.Flusher).Flush()


		for i:=0 ;i<10; i++{
			w.Write([]byte(fmt.Sprintf(`
                <h1>%d</h1>
            `,i)))
			w.(http.Flusher).Flush()
			time.Sleep(time.Duration(1) * time.Second)
		}

		w.Write([]byte(`
                    </body>
            </html>
        `))
		w.(http.Flusher).Flush()
	})
}
