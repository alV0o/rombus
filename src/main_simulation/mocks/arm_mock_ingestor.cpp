#include "rclcpp/rclcpp.hpp"
#include "rmf_ingestor_msgs/msg/ingestor_request.hpp"
#include "rmf_ingestor_msgs/msg/ingestor_result.hpp"
#include "string"
#include "set"

//заглушка робота-разгрузчика 
class ArmMockIngestor : public rclcpp::Node
{
public:
    ArmMockIngestor() : Node("arm_mock_ingestor")
    {
        
        this->declare_parameter<std::string>("rmf_ingestor_name", "default_arm");
        
        this->get_parameter("rmf_ingestor_name", name);
        
        RCLCPP_INFO(this->get_logger(), "Разгрузчик [%s] готов", name.c_str());
        
        request_subscription_ = this->create_subscription<rmf_ingestor_msgs::msg::IngestorRequest>(
        "ingestor_requests", 10, std::bind(&ArmMockIngestor::request_callback, this, std::placeholders::_1));
        result_publisher_ = this->create_publisher<rmf_ingestor_msgs::msg::IngestorResult>("ingestor_results", 10);
    }

private:
    void request_callback(const rmf_ingestor_msgs::msg::IngestorRequest::SharedPtr msg){
        if (msg->target_guid == name && used_requests.count(msg->target_guid) == 0){
            const auto first_item = msg->items[0];
            RCLCPP_INFO(this->get_logger(),
            "Разгрузчик [%s] получил запрос на разгрузку [%s] в количестве [%d]",
            name.c_str(),
            first_item.type_guid.c_str(),
            first_item.quantity);

            sleep(5);
            
            auto response = rmf_ingestor_msgs::msg::IngestorResult();
            response.request_guid = msg->request_guid;
            response.source_guid = msg->target_guid;
            response.status = rmf_ingestor_msgs::msg::IngestorResult::SUCCESS;
            result_publisher_->publish(response);
            RCLCPP_INFO(this->get_logger(), "Разгрузчик [%s] завершил разгрузку", name.c_str());

            used_requests.insert(msg->request_guid);

            if (used_requests.size() > 100){
                used_requests.erase(used_requests.begin());
            }
        }
    }
    std::string name;
    rclcpp::Subscription<rmf_ingestor_msgs::msg::IngestorRequest>::SharedPtr request_subscription_;
    rclcpp::Publisher<rmf_ingestor_msgs::msg::IngestorResult>::SharedPtr result_publisher_;
    std::set<std::string> used_requests;
};

int main(int argc, char ** argv){
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ArmMockIngestor>());
    rclcpp::shutdown();
    return 0;
}